from helper import *

#---- helpers

def make_df(tourn_130k_club_dict, skip_mins = True):
    all_tanks_df = pd.DataFrame()
    for tank_id, tourn_id in tourn_130k_club_dict.items():
        # tank
        tank_stats = get_tank_stats(tank_id, skip_mins = skip_mins)
        # tourn
        tourn_results = get_dict_from_url('https://tankpit.com/api/tournament_results?tournament_id=' + str(tourn_id), skip_mins = skip_mins)
        tourn_start_time = tourn_results['start_time_utc']
        #tourn_map = tourn_results['map']
        # make df
        tank_df = pd.DataFrame([tank_stats])
        tank_df['tourn_start_time'] = tourn_start_time
        tank_df['id'] = tank_id
        tank_df['tourn_id'] = tourn_id
        all_tanks_df = pd.concat([all_tanks_df, tank_df], axis = 0)
    all_tanks_df = all_tanks_df.reset_index(drop = True)
    # sort
    all_tanks_df = all_tanks_df.sort_values('tourn_start_time')
    # convert time
    all_tanks_df['tourn_start_time'] = pd.to_datetime(all_tanks_df['tourn_start_time']).dt.strftime("%b %-d, %Y")
    return(all_tanks_df)

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    tourn_130k_club_df = make_df(tourn_130k_club_dict)
    tourn_130k_club_df.to_csv(tourn_130k_club_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
