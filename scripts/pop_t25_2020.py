from pop_t100_overall import *

#----- main

if __name__ == '__main__':
    # load
    master_df = pd.read_csv(master_csv_2020).head(pop_t_2020_rows)
    passes_df = pd.read_csv(passes_csv_2020)
    passes_df = clean_passes_df(passes_df, pop_t_overall_rows)
    # pop
    with open(pop_t_2020_md, 'w') as f:
        f.write('\n## 2020 Top 25\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/t25-2020">Top 25</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-2020">Stats Leaderboard</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t25-2020-passes">Passes</a></p>\n\n')
        f.write('{:.t100}\n')
        f.write(get_tank_html(master_df))
        f.write('\n\n' + get_last_updated_html('Last Updated', time_now, time_now = True))
