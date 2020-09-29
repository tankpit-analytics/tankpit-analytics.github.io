from helper import *

#---- helpers

def get_cup_html(cup):
    if cup == 'gold':
        a = 3
    if cup == 'silver':
        a = 2
    if cup == 'bronze':
        a = 1
    cup_html = '<span class="awards-sprite a5-' + str(a) + '"></span>'
    return('<span class="awards-container">' + cup_html + '</span>')

def get_tank_html_i(master_df, i):
    i_id = master_df.loc[i, 'id']
    i_color = master_df.loc[i, 'color']
    i_name = master_df.loc[i, 'name']
    i_awards = master_df.loc[i, 'awards']
    i_awards_html = get_awards_html(i_awards)
    i_tourn_id = master_df.loc[i, 'tourn_id']
    i_tourn_start_time = master_df.loc[i, 'tourn_start_time']
    i_cup = master_df.loc[i, 'cup']
    i_cup_html = get_cup_html(i_cup)
    tank_html_i = '|<a target="_blank" href="https://tankpit.com/tournament_results/?tid=' + str(i_tourn_id) + '">' + str(i_tourn_start_time) + '</a>|' + i_cup_html + '|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) +\
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
    tourn_130k_club_df = pd.read_csv(tourn_130k_club_csv)
    # pop
    with open(pop_tourn_130k_club_md, 'w') as f:
        f.write('\n## 130k Club\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/cups-leaderboard">Cups Leaderboard</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="https://tankpit-analytics.github.io/130k-club">130k Club</a></p>\n\n')
        f.write('<p id="tourn_130k_club_criteria"><span id="criteria_bold">Criteria:</span><br />' + \
            '- Get 130k+ points<br />' + \
            '- Place 1st, 2nd, or 3rd<br />' + \
            '- Must be a 1 hour tournament' + \
            '</p>\n\n')
        f.write('{:.tourn_130k_club}\n')
        f.write('|<span class="tourn_130k_club_date">Date</span>|<span class="cup">&nbsp;</span>|<span class="tank_col">Tank</span>|\n')
        f.write(get_tank_html(tourn_130k_club_df))
