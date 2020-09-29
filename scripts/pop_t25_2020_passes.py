from pop_t100_overall_passes import *

#----- main

if __name__ == '__main__':
    # load and clean
    master_df = pd.read_csv(master_csv_2020)
    passes_df = pd.read_csv(passes_csv_2020)
    passes_df = clean_passes_df(passes_df, pop_t_2020_rows)
    passes_df = passes_df.head(pop_t_2020_passes_max_display)
    # get
    unique_master_tank_id_list = list(master_df['id'])
    unique_tank_id_list = list(set(list(passes_df['tank_id']) + list(passes_df['passed_tank_id'])))
    get_tank_id_list = [i for i in unique_tank_id_list if i not in unique_master_tank_id_list]
    unique_tank_dict = {}
    for tank_id in get_tank_id_list:
        unique_tank_dict[tank_id] = get_tank_stats(tank_id)
    # have
    have_tank_id_list = [i for i in unique_tank_id_list if i not in get_tank_id_list]
    for tank_id in have_tank_id_list:
        unique_tank_dict[tank_id] = get_tank_stats_from_master_df(master_df, tank_id)
    # pop
    with open(pop_t_2020_passes_md, 'w') as f:
        f.write('\n## 2020 Top 25 - Passes\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/t25-2020">Top 25</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t25-2020-passes">Passes</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-2020">Stats Leaderboard</a></p>\n\n')
        get_md(passes_df, unique_tank_dict, f, True)
        f.write('\n\n' + get_last_updated_html('Last Updated', time_now, time_now = True))
