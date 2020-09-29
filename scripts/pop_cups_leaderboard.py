from helper import *

#---- helpers

def get_html_i(df, i):
    i_id = df.loc[i, 'id']
    i_color = df.loc[i, 'color']
    i_name = df.loc[i, 'name']
    i_awards = df.loc[i, 'awards']
    i_awards_html = get_awards_html(i_awards)
    i_gold = df.loc[i, 'gold']
    i_silver = df.loc[i, 'silver']
    i_bronze = df.loc[i, 'bronze']
    i_total = df.loc[i, 'total']
    tank_html_i = '|' + str(i + 1) + '|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) +\
        '"><span class="' + str(i_color) + '">' + str(i_name) + '</span>' + str(i_awards_html) + '</a>|' + \
        str(i_gold) + '|' + str(i_silver) + '|' + str(i_bronze) + '|' + str(i_total) + '|\n'
    return(tank_html_i)

def get_html(df):
    tank_html = ''
    for i in range(len(df)):
        tank_html += get_html_i(df, i)
    return(tank_html)

#----- main

if __name__ == '__main__':
    cup_df = pd.read_csv(cup_counts_csv_2)
    cup_df = cup_df.head(pop_cups_leaderboard_max_display)
    last_updated_time = max(pd.to_datetime(cup_df['time_now']))
    # pop
    with open(pop_cups_leaderboard_md, 'w') as f:
        f.write('\n## Cups Leaderboard\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/cups-leaderboard">Cups Leaderboard</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="https://tankpit-analytics.github.io/130k-club">130k Club</a></p>\n\n')
        f.write('{:.cups_leaderboard}\n')
        f.write('|<span class="num_col">&nbsp;</span>|<span class="tank_col">Main Tank</span>|<span class="cup_col"><span class="awards-sprite a5-3"></span></span>|<span class="cup_col"><span class="awards-sprite a5-2"></span></span>|<span class="cup_col"><span class="awards-sprite a5-1"></span></span>|<span class="cup_col_total">Total</span>|\n')
        f.write(get_html(cup_df))
        f.write('\n\n' + get_last_updated_html('Last Updated', last_updated_time))
