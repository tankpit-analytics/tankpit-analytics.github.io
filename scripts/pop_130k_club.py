from helper import *

#---- helpers

def get_tank_html_i(master_df, i):
    i_id = master_df.loc[i, 'id']
    i_color = master_df.loc[i, 'color']
    i_name = master_df.loc[i, 'name']
    i_awards = master_df.loc[i, 'awards']
    i_awards_html = get_awards_html(i_awards)
    i_tourn_id = master_df.loc[i, 'tourn_id']
    i_tourn_start_time = master_df.loc[i, 'tourn_start_time']
    tank_html_i = '|<a target="_blank" href="https://tankpit.com/tournament_results/?tid=' + str(i_tourn_id) + '">' + str(i_tourn_start_time) + '</a>|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) +\
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
        f.write('{:.tourn_130k_club}\n')
        f.write('|<span class="tourn_130k_club_date">Date</span>|<span class="tank_col">Tank</span>|\n')
        f.write(get_tank_html(tourn_130k_club_df))
