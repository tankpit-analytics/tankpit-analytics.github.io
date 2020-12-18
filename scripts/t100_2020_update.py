from t100_main import *

#----- helpers

# supplement 2020 ladder updates with overall data
def supplement_passes_with_overall(master_csv_overall_file, master_csv_2020_file, passes_csv_2020_file, master_2020_nrow):
    print('##### SUPPLEMENT JOB')
    print(time_now)
    start_time = time.time()
    # load csvs
    master_df_overall = pd.read_csv(master_csv_overall_file)
    master_df_2020    = pd.read_csv(master_csv_2020_file)
    # only keep 2020 ids in master
    ids_2020    = list(master_df_2020['id'])
    master_df_overall_filtered = master_df_overall.loc[master_df_overall['id'].isin(ids_2020), :].reset_index(drop = True)
    print(master_df_2020.shape)
    print(master_df_overall_filtered.shape)
    # run supplement
    master_df_2020 = update_master_with_current(current_df = master_df_overall_filtered, master_df = master_df_2020, current_rank = 'unknown', passes_csv_file = passes_csv_2020_file)
    # save
    master_df_2020 = master_df_2020.head(master_2020_nrow)
    master_df_2020.to_csv(master_csv_2020_file, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    return(master_df_2020)

#----- main

if __name__ == '__main__':
    # master_df = update_all_ranks(
    #     leaderboard = '2020',
    #     master_csv_file = master_csv_2020,
    #     passes_csv_file = passes_csv_2020,
    #     ranks_dict = ranks_dict_2020,
    #     master_nrow = master_nrow_2020)
    # SUPPLEMENT JOB => currently in BETA - not being used
    master_df = supplement_passes_with_overall(
        master_csv_overall_file = master_csv_overall, 
        master_csv_2020_file = master_csv_2020,
        passes_csv_2020_file = passes_csv_2020,
        master_2020_nrow = master_nrow_2020)
