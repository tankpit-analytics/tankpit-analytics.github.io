from t100_main import *

#----- main

if __name__ == '__main__':
	start_5m_job_running()
    master_df = update_all_ranks(leaderboard = 'overall',
        master_csv_file = master_csv_overall,
        passes_csv_file = passes_csv_overall,
        ranks_dict = ranks_dict_overall,
        master_nrow = master_nrow_overall)
   	stop_5m_job_running()
