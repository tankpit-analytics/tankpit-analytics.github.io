from get_all_tanks_stats import *

#---- helpers

def run_half_loop(all_tanks):
    all_tanks['time_played'], all_tanks['destroyed_enemies'], all_tanks['deactivated'] = '', 0, 0
    for i in range(all_tanks.shape[0]):
        i_id = int(all_tanks.loc[i, 'id'])
        i_tank_dict = get_dict_from_url('https://tankpit.com/api/tank?tank_id=' + str(i_id), skip_mins = True)
        # i stats
        i_stats_dict = get_stats_dict(i_tank_dict)
        all_tanks = insert_stats_to_main_df(all_tanks, i_id, i_stats_dict)
    return(all_tanks)

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    # load and traverse
    y2020_tanks = pd.read_csv(y2020_tanks_csv)
    y2020_tanks = only_keep_has_any_award(y2020_tanks, awards_dict) # new addition - greatly reduces runtime
    y2020_tanks = rank_by_awards(y2020_tanks, awards_dict)
    y2020_tanks = run_half_loop(y2020_tanks)
    # save
    y2020_tanks.to_csv(y2020_tanks_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
