from t100_main import *

#----- helpers

# supplement 2022 ladder updates with overall data
def supplement_passes_with_overall(master_csv_overall_file, master_csv_2022_file, passes_csv_2022_file, master_2022_nrow):
    print('##### SUPPLEMENT JOB')
    print(time_now)
    start_time = time.time()
    # load csvs
    master_df_overall = pd.read_csv(master_csv_overall_file)
    master_df_2022    = pd.read_csv(master_csv_2022_file)
    # only keep 2022 ids in master
    ids_2022    = list(master_df_2022['id'])
    master_df_overall_filtered = master_df_overall.loc[master_df_overall['id'].isin(ids_2022), :].reset_index(drop = True)
    print(master_df_2022.shape)
    print(master_df_overall_filtered.shape)
    # run supplement
    master_df_2022 = update_master_with_current(current_df = master_df_overall_filtered, master_df = master_df_2022, current_rank = 'unknown', passes_csv_file = passes_csv_2022_file)
    # save
    master_df_2022 = master_df_2022.head(master_2022_nrow)
    master_df_2022.to_csv(master_csv_2022_file, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    return(master_df_2022)

#----- main

if __name__ == '__main__':
    master_df = update_all_ranks(
        leaderboard = '2022',
        master_csv_file = master_csv_2022,
        passes_csv_file = passes_csv_2022,
        ranks_dict = ranks_dict_2022,
        master_nrow = master_nrow_2022)
    # # SUPPLEMENT JOB => currently in BETA
    # master_df = supplement_passes_with_overall(
    #     master_csv_overall_file = master_csv_overall, 
    #     master_csv_2022_file = master_csv_2022,
    #     passes_csv_2022_file = passes_csv_2022,
    #     master_2022_nrow = master_nrow_2022)
