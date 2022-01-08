from helper import *

#---- helpers

def make_df(roster_col_list, skip_mins = True):
    all_tanks_df = pd.DataFrame()
    for i in range(len(roster_col_list)):
        tank_id = roster_col_list[i]
        # tank
        tank_stats = get_tank_stats(tank_id, skip_mins = skip_mins)
        tank_df = pd.DataFrame([tank_stats])
        tank_df['id'] = tank_id
        tank_df['i'] = i
        all_tanks_df = pd.concat([all_tanks_df, tank_df], axis = 0)
    all_tanks_df = all_tanks_df.sort_values('i')
    all_tanks_df = all_tanks_df.reset_index(drop = True)
    return(all_tanks_df)

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    roster_col_df = make_df(roster_col_list)
    roster_col_df.to_csv(roster_col_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
