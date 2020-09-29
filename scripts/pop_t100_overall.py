from pop_t100_overall_passes import *

#---- helpers

def get_tank_html_i(master_df, i):
    i_id = master_df.loc[i, 'id']
    i_color = master_df.loc[i, 'color']
    i_name = master_df.loc[i, 'name']
    i_awards = master_df.loc[i, 'awards']
    i_awards_html = get_awards_html(i_awards)
    tank_html_i = '|' + str(i + 1) + '|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) +\
        '"><span class="' + str(i_color) + '">' + str(i_name) + '</span>' + str(i_awards_html) + '</a>|\n'
    return(tank_html_i)

def get_tank_html(master_df):
    tank_html = ''
    for i in range(len(master_df)):
        tank_html += get_tank_html_i(master_df, i)
    return(tank_html)

#----- main

if __name__ == '__main__':
    # load
    master_df = pd.read_csv(master_csv_overall).head(pop_t_overall_rows)
    passes_df = pd.read_csv(passes_csv_overall)
    passes_df = clean_passes_df(passes_df, pop_t_overall_rows)
    # pop
    with open(pop_t_overall_md, 'w') as f:
        f.write('\n## True Top 100 Overall\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/">Top 100</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-overall">Stats Leaderboard</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t100-overall-passes">Passes</a></p>\n\n')
        f.write('{:.t100}\n')
        f.write(get_tank_html(master_df))
        f.write('\n\n' + get_last_updated_html('Last Updated', time_now, time_now = True))
