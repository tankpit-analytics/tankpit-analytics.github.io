from t100_main import *

#----- helpers

# supplement 2021 ladder updates with overall data
def supplement_passes_with_overall(master_csv_overall_file, master_csv_2021_file, passes_csv_2021_file, master_2021_nrow):
    print('##### SUPPLEMENT JOB')
    print(time_now)
    start_time = time.time()
    # load csvs
    master_df_overall = pd.read_csv(master_csv_overall_file)
    master_df_2021    = pd.read_csv(master_csv_2021_file)
    # only keep 2021 ids in master
    ids_2021    = list(master_df_2021['id'])
    master_df_overall_filtered = master_df_overall.loc[master_df_overall['id'].isin(ids_2021), :].reset_index(drop = True)
    print(master_df_2021.shape)
    print(master_df_overall_filtered.shape)
    # run supplement
    master_df_2021 = update_master_with_current(current_df = master_df_overall_filtered, master_df = master_df_2021, current_rank = 'unknown', passes_csv_file = passes_csv_2021_file)
    # save
    master_df_2021 = master_df_2021.head(master_2021_nrow)
    master_df_2021.to_csv(master_csv_2021_file, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    return(master_df_2021)

#----- main

if __name__ == '__main__':
    # master_df = update_all_ranks(
    #     leaderboard = '2021',
    #     master_csv_file = master_csv_2021,
    #     passes_csv_file = passes_csv_2021,
    #     ranks_dict = ranks_dict_2021,
    #     master_nrow = master_nrow_2021)
    # SUPPLEMENT JOB => currently in BETA
    master_df = supplement_passes_with_overall(
        master_csv_overall_file = master_csv_overall, 
        master_csv_2021_file = master_csv_2021,
        passes_csv_2021_file = passes_csv_2021,
        master_2021_nrow = master_nrow_2021)
