from pop_t100_overall import *

#----- main

if __name__ == '__main__':
    # load
    master_df = pd.read_csv(master_csv_2023).head(pop_t_2023_rows)
    passes_df = pd.read_csv(passes_csv_2023)
    passes_df = clean_passes_df(passes_df, pop_t_overall_rows)
    # pop
    with open(pop_t_2023_md, 'w') as f:
        f.write('\n## 2023 Top 25\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/t25-2023">Top 25</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t25-2023-passes">Passes</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-2023">Stats Leaderboard</a></p>\n\n')
        f.write('{:.t100}\n')
        f.write(get_tank_html(master_df))
        f.write('\n\n' + get_last_updated_html('Last Updated', time_now, time_now = True))
