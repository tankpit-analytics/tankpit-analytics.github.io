#incomplete!!!!!!!!













from get_all_tanks_stats import *

df_tourn_id_col = 'tourn_id'

#----- helpers

def check_is_done_tourn_id(tourn_id, df, df_tourn_id_col = df_tourn_id_col):
    try:
        if int(tourn_id) in list(df[df_tourn_id_col]):
            is_done = True
        else:
            is_done = False
    except:
        is_done = False
    return(is_done)

def get_tourn_results_dict(tourn_id):
    print('getting results for tourn_id:', str(tourn_id))
    return(get_dict_from_url('https://tankpit.com/api/tournament_results?tournament_id=' + str(tourn_id)))

#----- part 1. get tourn top3

# gets: (1) start time, (2) top 3 tank_id
def get_tourn_top3_df(tourn_id, df_tourn_id_col = df_tourn_id_col):
    tourn_dict = get_tourn_results_dict(tourn_id)
    start_time = tourn_dict['start_time_utc']
    first_place_tank_id = int(tourn_dict['results'][0]['tank_id'])
    second_place_tank_id = int(tourn_dict['results'][1]['tank_id'])
    third_place_tank_id = int(tourn_dict['results'][2]['tank_id'])
    df = pd.DataFrame({
            df_tourn_id_col: [int(tourn_id)],
            'start_time': [start_time],
            'first_place_tank_id': [first_place_tank_id],
            'second_place_tank_id': [second_place_tank_id],
            'third_place_tank_id': [third_place_tank_id]
        })
    df = df[[df_tourn_id_col, 'start_time', 'first_place_tank_id', 'second_place_tank_id', 'third_place_tank_id']]
    return(df)

def update_tourn_top3(df, tourn_id):
    if check_is_done_tourn_id(tourn_id, df) == False:
        try:
            tmp_df = get_tourn_top3_df(tourn_id)
            df = pd.concat([df, tmp_df], axis = 0)
        except:
            pass
    return(df)

def loop_update_tourn_top3(df, tourn_id_list, tourn_id_skip_list):
    tourn_id_list = [i for i in tourn_id_list if i not in tourn_id_skip_list]
    for tourn_id in tourn_id_list:
        df = update_tourn_top3(df, tourn_id)
    return(df)

#----- part 2. add to tourn monthly

#-- 2a. get signature tank_id

# reworked version of get_cup_count()+run_full_loop() in get_all_tank_stats.py: takes a tank_id and gets the best cup count checking all associated tanks until found
def get_best_cup_dict(tank_id, signature_cup_df, verbose = False):
    i_tank_dict, i_cup_dict, i_stats_dict = get_tank_cup_stats_dict(tank_id)
    # i+j = best cups [j stats within get_cup_count()]
    best_cup_dict = {'gold': 0, 'silver': 0, 'bronze': 0, 'total': 0}
    best_cups = 0
    i_cups = 0
    best_j_id = -1
    has_identified_signature = ''
    if i_cup_dict['total'] > 0:
        i_cups = i_cup_dict['total'] 
        best_cups = i_cups
        best_cup_dict = i_cup_dict
        j_count = 0
    else:
        # traverse through other tanks
        try:
            j_count = 0
            has_identified_signature_in_other_tanks_list = False
            for j_id in i_tank_dict['other_tanks']:
                if j_id in list(signature_cup_df['id']):
                    best_cup_dict = {
                        'gold': signature_cup_df[signature_cup_df['id'] == j_id, 'gold'],
                        'silver': signature_cup_df[signature_cup_df['id'] == j_id, 'silver'],
                        'bronze': signature_cup_df[signature_cup_df['id'] == j_id, 'bronze'],
                        'total': signature_cup_df[signature_cup_df['id'] == j_id, 'total']
                    }
                    has_identified_signature_in_other_tanks_list = True
                    break
            if has_identified_signature_in_other_tanks_list == True:
                j_count += 1
                has_identified_signature = '*****************************************'
                pass
            else:
                for j_id in i_tank_dict['other_tanks']:
                    j_count += 1
                    j_tank_dict, j_cup_dict, j_stats_dict = get_tank_cup_stats_dict(j_id)
                    # compare cup counts and choose best
                    j_cups = 0
                    if j_cup_dict['total'] > 0:
                        j_cups = j_cup_dict['total']
                    if j_cups > best_cups:
                        best_cups = j_cups
                        best_cup_dict = j_cup_dict
                        break
        except:
            pass
    if verbose == True:
        print('(tank_id: ' + str(tank_id) + ')', '- Number of other tanks checked:', j_count, has_identified_signature)
    return(best_cup_dict)

def find_signature_tank_id(tank_id, signature_cup_df, verbose = False):
    best_cup_dict = get_best_cup_dict(tank_id, signature_cup_df, verbose)
    try:
        signature_tank_id = int(signature_cup_df.loc[(signature_cup_df['gold'] == best_cup_dict['gold']) & 
                (signature_cup_df['silver'] == best_cup_dict['silver']) &
                (signature_cup_df['bronze'] == best_cup_dict['bronze']), 'id'])
    except:
        signature_tank_id = -1
    if verbose == True:
        print('signature tank: ' + str(signature_tank_id))
    return(signature_tank_id)














#----- main

# requires: cup_counts_csv_2
tourn_top3_csv = dir_tpdata + 'tourn_top3.csv'
tourn_top3_with_signature_csv = dir_tpdata + 'tourn_top3_with_signature.csv'
tourn_id_skip_list = [121, 126, 145, 157, 158, 177, 532, 544, 545, 672, 840, 851, 856, 869, 870, 871, 872, 1318, 1332, 1333, 1347]

if __name__ == '__main__':
    # part 1. get tourn top3 - DONE
    tourn_top3_df = pd.read_csv(tourn_top3_csv)
    # last_tourn_dict = get_dict_from_url('https://tankpit.com/api/last_finished_tournament')
    # last_tourn_id = int(last_tourn_dict['tournament_id'])
    # tourn_top3_df = loop_update_tourn_top3(tourn_top3_df, tourn_id_list = range(1, last_tourn_id), tourn_id_skip_list = tourn_id_skip_list)
    # tourn_top3_df.to_csv(tourn_top3_csv, index = False)
    # part 2. add to tourn monthly
    signature_cup_df = pd.read_csv(cup_counts_csv_2)
    tourn_top3_with_signature = pd.read_csv(tourn_top3_with_signature_csv)
    #
    #for i in range(len(tourn_top3_df)):
    for i in range(0,1000):
        print('#####', i)
        tmp_tourn_id = int(tourn_top3_df.loc[i, 'tourn_id'])
        if tmp_tourn_id not in list(tourn_top3_with_signature[df_tourn_id_col]):
            first_place_tank_id = tourn_top3_df.loc[i, 'first_place_tank_id']
            first_place_signature_tank_id = find_signature_tank_id(first_place_tank_id, signature_cup_df, verbose = True)
            second_place_tank_id = tourn_top3_df.loc[i, 'second_place_tank_id']
            second_place_signature_tank_id = find_signature_tank_id(second_place_tank_id, signature_cup_df, verbose = True)
            third_place_tank_id = tourn_top3_df.loc[i, 'third_place_tank_id']
            third_place_signature_tank_id = find_signature_tank_id(third_place_tank_id, signature_cup_df, verbose = True) 
            tmp_df = pd.DataFrame({
                        df_tourn_id_col: [tmp_tourn_id],
                        'start_time': [tourn_top3_df.loc[i, 'start_time']],
                        'first_place_signature_tank_id': [first_place_signature_tank_id],
                        'second_place_signature_tank_id': [second_place_signature_tank_id],
                        'third_place_signature_tank_id': [third_place_signature_tank_id]
                    })
            tmp_df = tmp_df[[df_tourn_id_col, 'start_time', 'first_place_signature_tank_id', 'second_place_signature_tank_id', 'third_place_signature_tank_id']]
            tourn_top3_with_signature = pd.concat([tourn_top3_with_signature, tmp_df], axis = 0)
    #
    tourn_top3_with_signature.to_csv(tourn_top3_with_signature_csv, index = False)
    
















