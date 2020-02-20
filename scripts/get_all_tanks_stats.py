from helper import *

#---- helpers

def get_cup_dict(tank_dict):
    cup_dict = {}
    try:
        cup_dict['gold'] = int(tank_dict['user_tournament_victories']['gold'])
        cup_dict['silver'] = int(tank_dict['user_tournament_victories']['silver'])
        cup_dict['bronze'] = int(tank_dict['user_tournament_victories']['bronze'])
        cup_dict['total'] = int(cup_dict['gold'] + cup_dict['silver'] + cup_dict['bronze'])
    except:
        pass
    return(cup_dict)

def get_stats_dict(tank_dict):
    stats_dict = {'time_played': '0:0:0', 'destroyed_enemies': 0, 'deactivated': 0}
    try:
        stats_dict['time_played'] = tank_dict['map_data']['World']['time_played']
        stats_dict['destroyed_enemies'] = tank_dict['map_data']['World']['destroyed_enemies']
        stats_dict['deactivated'] = tank_dict['map_data']['World']['deactivated']
    except:
        pass
    return(stats_dict)

def insert_cup_counts_to_main_df(main_df, i_id, cup_dict):
    main_df.loc[main_df['id'] == i_id, 'gold'] = cup_dict['gold']
    main_df.loc[main_df['id'] == i_id, 'silver'] = cup_dict['silver']
    main_df.loc[main_df['id'] == i_id, 'bronze'] = cup_dict['bronze']
    main_df.loc[main_df['id'] == i_id, 'total'] = cup_dict['total']
    return(main_df)

def insert_stats_to_main_df(main_df, i_id, stats_dict):
    main_df.loc[main_df['id'] == i_id, 'time_played'] = stats_dict['time_played']
    main_df.loc[main_df['id'] == i_id, 'destroyed_enemies'] = stats_dict['destroyed_enemies']
    main_df.loc[main_df['id'] == i_id, 'deactivated'] = stats_dict['deactivated']
    return(main_df)

def get_cup_count(i, all_tanks, i_tank_dict, done_ids, verbose = False):
    i_cup_dict = get_cup_dict(i_tank_dict)
    best_cup_dict = {'gold': 0, 'silver': 0, 'bronze': 0, 'total': 0}
    best_cups = 0
    i_cups = 0
    if len(i_cup_dict) > 0:
        i_cups = i_cup_dict['total'] 
        best_cups = i_cups
        best_cup_dict = i_cup_dict
    # traverse through other tanks
    try:
        j_count = 0
        for j_id in i_tank_dict['other_tanks']:
            j_count += 1
            done_ids.append(j_id)
            j_tank_dict = get_dict_from_url('https://tankpit.com/api/tank?tank_id=' + str(j_id))
            # j cups
            j_cup_dict = get_cup_dict(j_tank_dict)
            # j stats
            j_stats_dict = get_stats_dict(j_tank_dict)
            all_tanks = insert_stats_to_main_df(all_tanks, j_id, j_stats_dict)
            # compare cup counts and choose best
            j_cups = 0
            if len(j_cup_dict) > 0:
                j_cups = j_cup_dict['total']
            if j_cups > best_cups:
                best_cups = j_cups
                best_cup_dict = j_cup_dict
    except:
        pass
    # add cup count to main df
    if verbose == True:
        print(i, j_count)
    return(best_cup_dict, done_ids, all_tanks)

def run_full_loop(all_tanks, verbose = False):
    all_tanks['gold'], all_tanks['silver'], all_tanks['bronze'], all_tanks['total'] = 0, 0, 0, 0
    all_tanks['time_played'], all_tanks['destroyed_enemies'], all_tanks['deactivated'] = '0:0:0', 0, 0
    done_ids = []
    for i in range(all_tanks.shape[0]):
        i_id = int(all_tanks.loc[i, 'id'])
        if i_id not in done_ids:
            done_ids.append(i_id)
            i_tank_dict = get_dict_from_url('https://tankpit.com/api/tank?tank_id=' + str(i_id))
            # i+j = best cups [j stats within get_cup_count()]
            best_cup_dict, done_ids, all_tanks = get_cup_count(i, all_tanks, i_tank_dict, done_ids, verbose)
            all_tanks = insert_cup_counts_to_main_df(all_tanks, i_id, best_cup_dict)
            # i stats
            i_stats_dict = get_stats_dict(i_tank_dict)
            all_tanks = insert_stats_to_main_df(all_tanks, i_id, i_stats_dict)
    return(all_tanks)

def clean_cup_df_1(df):
    # drop tanks with 0 cups shown in profile
    df = df[df['total'] > 0].reset_index(drop = True)
    # sort by total > gold > silver > bronze > id
    df = df.sort_values(['total','gold','silver','bronze','id'], ascending = [False,False,False,False,True]).reset_index(drop = True)
    return(df)

def clean_cup_df_2(df):
    # drop duplicates
    df = df.drop_duplicates(['gold','silver','bronze'], keep = 'first').reset_index(drop = True)
    return(df)

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    # load and traverse
    all_tanks = pd.read_csv(all_tanks_csv)
    all_tanks = rank_by_awards(all_tanks, awards_dict)
    all_tanks = run_full_loop(all_tanks)
    # save
    all_tanks.to_csv(all_tanks_csv, index = False)
    # clean
    cup_df_1 = clean_cup_df_1(all_tanks)
    cup_df_2 = clean_cup_df_2(cup_df_1)
    # save
    cup_df_1.to_csv(cup_counts_csv_1, index = False)
    cup_df_2.to_csv(cup_counts_csv_2, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
