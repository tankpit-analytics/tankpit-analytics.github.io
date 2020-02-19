from t100_main import *

#---- helpers

def get_all_tanks(ranks_dict, get_leaderboard = 'overall'):
    tanks_2012 = get_df_for_x_pages_from_api(leaderboard = '2012', pages = 1, max_pages = True, rank = 'general')
    tank_ids_2012 = list(tanks_2012['id'])
    tank_ids_2012 = [int(i) for i in tank_ids_2012]
    df = pd.DataFrame()
    for rank in ranks_dict.keys():
        tmp_df = get_df_for_x_pages_from_api(leaderboard = get_leaderboard, pages = 1, max_pages = True, rank = rank)
        df = pd.concat([df, tmp_df], axis = 0).reset_index(drop = True)
    df = df.dropna().reset_index(drop = True)
    # remove 2012 tanks
    df = df[~df['id'].isin(tank_ids_2012)].reset_index(drop = True)
    return(df)

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    all_tanks = get_all_tanks(ranks_dict_overall)
    all_tanks['time_now'] = time_now
    all_tanks.to_csv(all_tanks_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
