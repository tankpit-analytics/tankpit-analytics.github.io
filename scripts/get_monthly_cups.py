#incomplete!!!!!!!!













from helper import *

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

# gets: (1) start time, (2) top 3 tank_id
def get_tourn_top3_df(tourn_id, df_tourn_id_col = df_tourn_id_col):
    tourn_dict = get_tourn_results_dict(tourn_id)
    start_time = tourn_dict['start_time_utc']
    first_place_tank_id = int(tourn_dict['results'][0]['tank_id'])
    second_place_tank_id = int(tourn_dict['results'][1]['tank_id'])
    third_place_tank_id = int(tourn_dict['results'][2]['tank_id'])
    return(pd.DataFrame({
            df_tourn_id_col: [int(tourn_id)],
            'start_time': [start_time],
            'first_place_tank_id': [first_place_tank_id],
            'second_place_tank_id': [second_place_tank_id],
            'third_place_tank_id': [third_place_tank_id]
        }))

#----- part 1. get tourn top3

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

#def get_cup_count():




#----- main

# requires: cup_counts_csv_2
tourn_top3_csv = dir_tpdata + 'tourn_top3.csv'
tourn_id_skip_list = [121, 126, 145, 157, 158, 177, 532, 544, 545, 672, 840, 851, 856, 869, 870, 871, 872, 1318, 1332, 1333, 1347]

def get_dict_from_url(link, skip_mins = False, max_tries = api_max_tries):
    for tries in range(1, max_tries + 1):
        # daily job
        if skip_mins == True:
            if check_is_5m_job_running():
                # don't run
                add_delay(5)
                print('... 5m job running, delaying daily job for 5 seconds.', str(datetime.now()))
            else:
                # run!
                response = get_request(link)
                if response.status_code == 200:
                    break
                if response.status_code == 404:
                    print(tries, 'GET request error (' + str(response.status_code) + '):', link, str(datetime.now()))
                    break              
                print(tries, 'GET request error (' + str(response.status_code) + '), trying again for:', link, str(datetime.now()))
        # 5min job
        else:
            response = get_request(link)
            if response.status_code == 200:
                break
            if response.status_code == 404:
                print(tries, 'GET request error (' + str(response.status_code) + '):', link, str(datetime.now()))
                break
            print(tries, 'GET request error (' + str(response.status_code) + '), trying again for:', link, str(datetime.now()))
    response_dict = response.json()
    return(response_dict)

if __name__ == '__main__':
    # part 1. get tourn top3
    tourn_top3_df = pd.read_csv(tourn_top3_csv)
    last_tourn_dict = get_dict_from_url('https://tankpit.com/api/last_finished_tournament')
    last_tourn_id = int(last_tourn_dict['tournament_id'])
    tourn_top3_df = loop_update_tourn_top3(tourn_top3_df, tourn_id_list = range(1, last_tourn_id), tourn_id_skip_list = tourn_id_skip_list)
    tourn_top3_df.to_csv(tourn_top3_csv, index = False)
    # part 2. add to tourn monthly
    #
    #signature_cup_df = pd.read_csv(cup_counts_csv_2)
















