from helper import *

#---- helpers

def get_active_df(active_dict):
    for i in active_dict:
        if i['name'].find('World') != -1:
            world_map = i['map']
            world_playing = i['playing_tanks']
            world_waiting = i['waiting_tanks']
        if i['name'].find('Practice') != -1:
            practice_map = i['map']
            practice_playing = i['playing_tanks']
            practice_waiting = i['waiting_tanks']
    tmp_df = pd.DataFrame([{'time_now': time_now,
        'world_map': world_map, 'world_playing': world_playing, 'world_waiting': world_waiting,
        'practice_map': practice_map, 'practice_playing': practice_playing, 'practice_waiting': practice_waiting}])
    return(tmp_df)

#----- main

if __name__ == '__main__':
    start_5m_job_running()
    print('#####')
    print(time_now)
    start_time = time.time()
    try:
        active_df = pd.read_csv(active_csv)
    except:
        active_df = pd.DataFrame()
    active_dict = get_dict_from_url('https://tankpit.com/api/active_games')
    tmp_df = get_active_df(active_dict)
    active_df = pd.concat([active_df, tmp_df], axis = 0).reset_index(drop = True)
    active_df.to_csv(active_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    stop_5m_job_running()
