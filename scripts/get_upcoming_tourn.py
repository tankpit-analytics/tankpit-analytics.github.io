from helper import *

#---- helpers

def get_upcoming_tourn_df(upcoming_tourn_dict):
    upcoming_tourn_dict = upcoming_tourn_dict[0]
    start_time = upcoming_tourn_dict['start_time_utc']
    end_time = upcoming_tourn_dict['end_time_utc']
    tmap = upcoming_tourn_dict['map']
    tmp_df = pd.DataFrame([{'time_now': time_now,
        'start_time': start_time, 'end_time': end_time, 'tmap': tmap}])
    return(tmp_df)

#----- main

if __name__ == '__main__':
    start_5m_job_running()
    print('#####')
    print(time_now)
    start_time = time.time()
    try:
        upcoming_tourn_df = pd.read_csv(upcoming_tourn_csv)
    except:
        upcoming_tourn_df = pd.DataFrame()
    upcoming_tourn_dict = get_dict_from_url('https://tankpit.com/api/upcoming_tournaments')
    tmp_df = get_upcoming_tourn_df(upcoming_tourn_dict)
    upcoming_tourn_df = pd.concat([upcoming_tourn_df, tmp_df], axis = 0).reset_index(drop = True)
    upcoming_tourn_df.to_csv(upcoming_tourn_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    stop_5m_job_running()
