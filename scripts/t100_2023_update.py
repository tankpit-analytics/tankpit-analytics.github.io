from t100_main import *

#----- helpers

# supplement 2023 ladder updates with overall data
def supplement_passes_with_overall(master_csv_overall_file, master_csv_2023_file, passes_csv_2023_file, master_2023_nrow):
    print('##### SUPPLEMENT JOB')
    print(time_now)
    start_time = time.time()
    # load csvs
    master_df_overall = pd.read_csv(master_csv_overall_file)
    master_df_2023    = pd.read_csv(master_csv_2023_file)
    # only keep 2023 ids in master
    ids_2023    = list(master_df_2023['id'])
    master_df_overall_filtered = master_df_overall.loc[master_df_overall['id'].isin(ids_2023), :].reset_index(drop = True)
    print(master_df_2023.shape)
    print(master_df_overall_filtered.shape)
    # run supplement
    master_df_2023 = update_master_with_current(current_df = master_df_overall_filtered, master_df = master_df_2023, current_rank = 'unknown', passes_csv_file = passes_csv_2023_file)
    # save
    master_df_2023 = master_df_2023.head(master_2023_nrow)
    master_df_2023.to_csv(master_csv_2023_file, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    return(master_df_2023)

#----- main

if __name__ == '__main__':
    master_df = update_all_ranks(
        leaderboard = '2023',
        master_csv_file = master_csv_2023,
        passes_csv_file = passes_csv_2023,
        ranks_dict = ranks_dict_2023,
        master_nrow = master_nrow_2023)
    # # SUPPLEMENT JOB => currently in BETA
    # master_df = supplement_passes_with_overall(
    #     master_csv_overall_file = master_csv_overall, 
    #     master_csv_2023_file = master_csv_2023,
    #     passes_csv_2023_file = passes_csv_2023,
    #     master_2023_nrow = master_nrow_2023)
