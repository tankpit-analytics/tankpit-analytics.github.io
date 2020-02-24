from helper import *

# a little slower but more accurate
j_loop = True

#----- functions 1: API

def get_df_from_leaderboard_dict(tmp_dict):
    l_df = pd.DataFrame(tmp_dict['results'])
    l_df = l_df[['tank_id', 'name', 'awards', 'color']]
    l_df = l_df.rename(columns = {'tank_id': 'id'})
    return(l_df)

# max_pages == True will ignore pages
def get_df_for_x_pages_from_api(leaderboard,
                                skip_mins = False,
                                pages = 1,
                                max_pages = False,
                                rank = 'general'):
    url = 'https://tankpit.com/api/leaderboards/?leaderboard=' + leaderboard + '&rank=' + rank + '&page='
    # get max pages, reconcile with pages param
    m_dict = get_dict_from_url(url + '1', skip_mins)
    m_pages = int(m_dict['total_pages'])
    if (max_pages == True) | (m_pages < pages):
        pages = m_pages
    # loop through pages
    p_df = pd.DataFrame()
    for page in range(pages):
        # no need to fetch 1st page again
        if page == 0:
            p_dict = m_dict
        else:
            p_dict = get_dict_from_url(url + str(page + 1))
        p_tmp_df = get_df_from_leaderboard_dict(p_dict)
        p_df = pd.concat([p_df, p_tmp_df], axis = 0).reset_index(drop = True)
    return(p_df)

#----- functions 2: data manipulation helpers

def df_swap_rows(df, index_1, index_2):
    c = df.iloc[index_1].copy()
    df.iloc[index_1] = df.iloc[index_2]
    df.iloc[index_2] = c
    return(df)

def df_insert_row(df, new_row, old_row):
    for v in reversed(range(new_row, old_row)):
        index_1 = v
        index_2 = v + 1
        df = df_swap_rows(df, index_1, index_2)
    return(df)

#----- functions 3: csv

# add new row to passes.csv
def add_to_passes(i_id, i_action, p, new_row, passes_csv_file, time_now = time_now):
    try:
        passes_df = pd.read_csv(passes_csv_file)
    except:
        passes_df = pd.DataFrame()
    tmp_df = pd.DataFrame([{'tank_id': i_id, 'passed_tank_id': p, 'time': time_now, 'new_row': new_row, 'action': i_action}])
    tmp_df = tmp_df[['time', 'action', 'tank_id', 'passed_tank_id', 'new_row']]
    passes_df = pd.concat([passes_df, tmp_df], axis = 0)
    passes_df.reset_index(drop = True, inplace = True)
    passes_df.to_csv(passes_csv_file, index = False)

#----- functions 4: updates

# update rows in master df- below functions need this
def update_passes_in_master(i_id, i_index_master, master_df, rank_paren, just_added, i_confirmed, i_passed_index_list, i_passed_id_list, passes_csv_file, time_now = time_now):
    if len(i_passed_id_list) > 0:
        old_row = int(i_index_master[0])
        new_row = min(i_passed_index_list)
        master_df = df_insert_row(master_df, new_row, old_row)
        for p in reversed(i_passed_id_list):
            i_action = None
            if not just_added:
                if i_confirmed:
                    print(i_id, 'passed', p, rank_paren)
                    i_action = 'pass ' + rank_paren
                if not i_confirmed:
                    print(i_id, 'corrected ahead of', p, rank_paren)
                    i_action = 'correction ' + rank_paren
            if just_added:
                print(i_id, 'just added to master ahead of', p, rank_paren)
                i_action = 'just added to master ' + rank_paren
            add_to_passes(i_id, i_action, p, new_row, passes_csv_file)
    return(master_df)

# j-loop: takes longer to run and theoretically should no longer need to be running after data converges a few weeks in - if using this, no need to use non-j-loop
def update_passes_j_loop(i, i_id, i_index_master, new_df, master_df, rank_paren, just_added, i_confirmed, passes_csv_file):
    # not a bot
    if i_id > 36:
        i_passed_index_list = []
        i_passed_id_list = []
        for j in range(i + 1, len(new_df)):
            j_id = int(new_df.loc[j, 'id'])
            # not a bot
            if j_id > 36: 
                j_index_master = master_df.loc[master_df['id'] == j_id, :].index
                # if j is in master
                if len(j_index_master) == 1:
                    # was j ahead of i in master? (ahead = lower index)
                    if j_index_master < i_index_master:
                        # list of all the j's that i passed
                        i_passed_index_list.append(int(j_index_master[0]))
                        i_passed_id_list.append(j_id)
                        # break as soon as it finds a j
                        break
        master_df = update_passes_in_master(i_id, i_index_master, master_df, rank_paren, just_added, i_confirmed, i_passed_index_list, i_passed_id_list, passes_csv_file)
    return(master_df)

# non-j-loop: modified to only look at j directly behind i
def update_passes(i, i_id, i_index_master, new_df, master_df, rank_paren, just_added, i_confirmed, passes_csv_file):
    # not a bot
    if i_id > 36:
        i_passed_index_list = []
        i_passed_id_list = []
        j = i + 1
        j_id = int(new_df.loc[j, 'id'])
        # not a bot
        if j_id > 36:   
            j_index_master = master_df.loc[master_df['id'] == j_id, :].index
            # if j is in master
            if len(j_index_master) == 1:
                # was j ahead of i in master? (ahead = lower index)
                if j_index_master < i_index_master:
                    # list of all the j's that i passed
                    i_passed_index_list.append(int(j_index_master[0]))
                    i_passed_id_list.append(j_id)
        master_df = update_passes_in_master(i_id, i_index_master, master_df, rank_paren, just_added, i_confirmed, i_passed_index_list, i_passed_id_list, passes_csv_file)
    return(master_df)

# modified to use both k (tank before) + j (tank after) - if using, this should go after updating passes
def update_confirmed_k_j(i, i_id, i_index_master, new_df, master_df, rank_paren, i_confirmed, passes_csv_file):
    # not a bot
    if i_id > 36:
        i_passed_index_list = []
        i_passed_id_list = []
        j = i + 1
        j_id = int(new_df.loc[j, 'id'])
        # not a bot
        if j_id > 36:   
            j_index_master = master_df.loc[master_df['id'] == j_id, :].index
            # if j is in master
            if len(j_index_master) == 1:
                # if j is directly behind i in master and j is confirmed
                if ((i_index_master + 1) == j_index_master) & (list(master_df.loc[master_df['id'] == j_id, 'confirmed'])[0]):
                    k = i - 1
                    k_id = int(new_df.loc[k, 'id'])
                    # not a bot
                    if k_id > 36:
                        k_index_master = master_df.loc[master_df['id'] == k_id, :].index
                        # if k is in master
                        if len(k_index_master) == 1:
                            # if k is directly ahead of i in master and k is confirmed
                            if ((k_index_master + 1) == i_index_master) & (list(master_df.loc[master_df['id'] == k_id, 'confirmed'])[0]):   
                                if not i_confirmed:
                                    # if here, then wasn't confirmed before, but not confirmed
                                    print(i_id, 'confirmed', rank_paren)
                                    i_action = 'confirmed ' + rank_paren
                                    master_df.loc[master_df['id'] == i_id, 'confirmed'] = True
                                    add_to_passes(i_id, i_action, p = j_id, new_row = i_index_master, passes_csv_file = passes_csv_file)
    return(master_df)

def add_to_master(i_id, new_df, master_df):
    i_confirmed = False
    # append to the end of master
    tmp_df = new_df.loc[new_df['id'] == i_id, :].copy()
    tmp_df.reset_index(drop = True, inplace = True)
    tmp_df['confirmed'] = i_confirmed
    tmp_df = tmp_df[['awards', 'color', 'id', 'name', 'confirmed']]
    master_df = pd.concat([master_df, tmp_df], axis = 0, sort = False)
    master_df.reset_index(drop = True, inplace = True)
    return(master_df)

def update_master_with_current(current_df, master_df, current_rank, passes_csv_file, j_loop = j_loop):
    for i in range(len(current_df)):
        just_added = False
        i_id = int(current_df.loc[i, 'id'])
        i_index_master = master_df.loc[master_df['id'] == i_id, :].index
        # not a bot
        if i_id > 36:
            # if i is not in master, add to master
            if len(i_index_master) == 0:
                master_df = add_to_master(i_id, current_df, master_df)
                i_index_master = master_df.loc[master_df['id'] == i_id, :].index
                just_added = True
            i_confirmed = list(master_df.loc[master_df['id'] == i_id, 'confirmed'])[0]
            # if rank is general, then confirmed
            if (current_rank == 'general') & (not i_confirmed):
                print(i_id, 'confirmed (general)')
                master_df.loc[master_df['id'] == i_id, 'confirmed'] = True
                i_confirmed = True
                i_action = 'confirmed (general)'
                add_to_passes(i_id, i_action, p = None, new_row = None, passes_csv_file = passes_csv_file)
            # if i is not last one
            if i + 1 != len(current_df):
                rank_paren = '(' + str(current_rank) + ')'
                # 1. check for passes
                if j_loop == True:
                    master_df = update_passes_j_loop(i, i_id, i_index_master, current_df, master_df, rank_paren, just_added, i_confirmed, passes_csv_file)
                if j_loop == False:
                    master_df = update_passes(i, i_id, i_index_master, current_df, master_df, rank_paren, just_added, i_confirmed, passes_csv_file)
                # 2. check for confirmation, cannot do this if i is first one
                i_index_master = master_df.loc[master_df['id'] == i_id, :].index
                if (i != 0) & (not i_confirmed):
                    master_df = update_confirmed_k_j(i, i_id, i_index_master, current_df, master_df, rank_paren, i_confirmed, passes_csv_file)
            # updating name, awards, color
            if i_id in list(master_df['id']):
                master_df.loc[master_df['id'] == i_id, 'name'] = current_df.loc[i, 'name']
                master_df.loc[master_df['id'] == i_id, 'awards'] = str(current_df.loc[i, 'awards'])
                master_df.loc[master_df['id'] == i_id, 'color'] = current_df.loc[i, 'color']
    return(master_df)

#----- functions 5: main

def update_all_ranks(leaderboard, master_csv_file, passes_csv_file, ranks_dict, master_nrow, time_now = time_now):
    print('#####')
    print(time_now)
    start_time = time.time()
    master_df = pd.read_csv(master_csv_file).head(master_nrow)
    for rank, pages in ranks_dict.items():
        current_df = get_df_for_x_pages_from_api(leaderboard, pages = pages, max_pages = False, rank = rank)
        master_df = update_master_with_current(current_df, master_df, rank, passes_csv_file)
    # save
    master_df = master_df.head(master_nrow)
    master_df.to_csv(master_csv_file, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    return(master_df)

# only run this the very first time
def initial_run(leaderboard, master_csv_file, master_nrow):
    start_time = time.time()
    master_df = get_df_for_x_pages_from_api(leaderboard, pages = 1, max_pages = True, rank = 'general')
    master_df['confirmed'] = True
    master_df = master_df.head(master_nrow)
    master_df.to_csv(master_csv_file, index = False)
    elapsed_time = time.time() - start_time
    print('Runtime:', round(elapsed_time, 1), 'seconds')
    return(master_df)
