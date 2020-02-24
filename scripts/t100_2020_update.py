from t100_main import *

#----- main

if __name__ == '__main__':
    start_5m_job_running()
    master_df = update_all_ranks(
        leaderboard = '2020',
        master_csv_file = master_csv_2020,
        passes_csv_file = passes_csv_2020,
        ranks_dict = ranks_dict_2020,
        master_nrow = master_nrow_2020)
    stop_5m_job_running()
