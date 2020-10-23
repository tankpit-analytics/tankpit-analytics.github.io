from helper import *

import pickle
import os

#---- helpers, part 1: concat new backups

def concat_new_backups(backups_concat_df, dir_backups, done_filenames_list):
    for filename in os.listdir(dir_backups):
        if filename.startswith('all_tanks') and filename not in done_filenames_list:
            # add to backups_concat_df
            tmp_df = pd.read_csv(dir_backups + filename)
            backups_concat_df = pd.concat([backups_concat_df, tmp_df], axis = 0).reset_index(drop = True)
            # add to done_filenames_list
            done_filenames_list.append(filename)
    return(backups_concat_df, done_filenames_list)

#---- helpers, part 2: find new decorations

def get_recent_df(backups_concat_df, run_alltime = False, lookback_days = 7):
    # munge 
    backups_concat_df['time_now'] = pd.to_datetime(backups_concat_df['time_now'])
    # date of interest (this date + look back 7 days)
    date_of_interest_max = datetime.now() + timedelta(days = 1) # add a day just in case
    if run_alltime == False:
        date_of_interest_min = date_of_interest_max - timedelta(days = lookback_days)
        recent_backups_concat_df = backups_concat_df[(backups_concat_df['time_now'] >= date_of_interest_min) & ((backups_concat_df['time_now'] <= date_of_interest_max))]
    else:
        recent_backups_concat_df = backups_concat_df
    return(recent_backups_concat_df)

def extract_latest_decorations_from_recent_df(recent_df):
    latest_awards_list = []
    tank_ids_with_multiple_entries = list((recent_df.groupby('id').count()['name'] > 1).index)
    for tank_id in tank_ids_with_multiple_entries:
        recent_df_i = recent_df[recent_df['id'] == tank_id]
        recent_df_i = recent_df_i.sort_values('time_now', ascending = False).reset_index(drop = True)
        for i in range(recent_df_i.shape[0]):
            if i < recent_df_i.shape[0] - 2:
                awards = recent_df_i.loc[i, 'awards']
                previous_awards = recent_df_i.loc[i + 1, 'awards']
                if awards != previous_awards:
                    award_time = recent_df_i.loc[i, 'time_now']
                    tank_id = recent_df_i.loc[i, 'id']
                    latest_awards_list.append({'tank_id': tank_id,
                                               'awards': awards,
                                               'previous_awards': previous_awards,
                                               'award_time': award_time})
    # single shining sword - INCOMPLETE... DO THIS AT SOME POINT
    #tank_ids_without_multiple_entries = list(recent_df.loc[~recent_df['id'].isin(tank_ids_with_multiple_entries), 'id'])
    return(latest_awards_list)

def convert_latest_decorations(latest_awards_list):
    latest_awards_converted_list = []
    for decoration in latest_awards_list:
        for i in range(len(decoration['awards'])):
            if decoration['awards'][i] != decoration['previous_awards'][i]:
                latest_awards_converted_list.append({'tank_id': decoration['tank_id'],
                                                     'award_time': decoration['award_time'],
                                                     'award': award_string_conversion[i],
                                                     'tier': int(decoration['awards'][i])})
    return(latest_awards_converted_list)

#----- main

if __name__ == '__main__':
    print('#####')
    print(time_now)
    start_time = time.time()
    #-- part 1: concat new backups
    # 1. load files
    with open(done_filenames_list_pickle, 'rb') as f:
        done_filenames_list = pickle.load(f)
    with open(backups_concat_pickle, 'rb') as f:
        backups_concat_df = pickle.load(f)
    # 2. update backups_concat_df with new backups
    backups_concat_df, done_filenames_list = concat_new_backups(backups_concat_df, dir_backups, done_filenames_list)
    # 3. save files
    with open(done_filenames_list_pickle, 'wb') as f:
        pickle.dump(done_filenames_list, f) 
    with open(backups_concat_pickle, 'wb') as f:
        pickle.dump(backups_concat_df, f)
    #-- part 2: find new decorations
    # 1. get recent df
    recent_backups_concat_df = get_recent_df(backups_concat_df, run_alltime = False, lookback_days = lookback_days)
    # 2. extract & convert
    latest_awards_list = extract_latest_decorations_from_recent_df(recent_backups_concat_df)
    latest_awards_converted_list = convert_latest_decorations(latest_awards_list)
    award_decorations_df = pd.DataFrame(latest_awards_converted_list)
    # 3. load master, concat, de-dupe
    master_award_decorations_df = pd.read_csv(master_award_decorations_csv)
    master_award_decorations_df = pd.concat([master_award_decorations_df, award_decorations_df], axis = 0, sort = True)
    master_award_decorations_df = master_award_decorations_df.drop_duplicates(subset = ['award','tank_id','tier'], keep = 'first')
    master_award_decorations_df['award_time'] = pd.to_datetime(master_award_decorations_df['award_time'])
    master_award_decorations_df = master_award_decorations_df.sort_values('award_time', ascending = False).reset_index(drop = True)
    # 4. save master
    master_award_decorations_df.to_csv(master_award_decorations_csv, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
