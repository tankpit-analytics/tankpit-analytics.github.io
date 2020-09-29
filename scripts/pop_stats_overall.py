from helper import *

#---- helpers

def extract_time(df, time_col = 'time_played'):
    df = df.reset_index(drop = False)
    time_df = df[time_col].str.extract(r'(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)').reset_index(drop = False)
    time_df['hours'] = time_df['hours'].fillna(0)
    time_df['minutes'] = time_df['minutes'].fillna(0)
    time_df['seconds'] = time_df['seconds'].fillna(0)
    time_df['hours'] = time_df['hours'].astype(int)
    time_df['minutes'] = time_df['minutes'].astype(int)
    time_df['seconds'] = time_df['seconds'].astype(int)
    df = df.merge(time_df, how = 'inner', on = 'index')
    df['total_seconds'] = (df['hours'] * 60 * 60) + (df['minutes'] * 60) + df['seconds']
    df = df.drop('index', axis = 1)
    return(df)

def get_html_i(df, i, stat = 'time_played'):
    i_id = df.loc[i, 'id']
    i_color = df.loc[i, 'color']
    i_name = df.loc[i, 'name']
    i_awards = df.loc[i, 'awards']
    i_awards_html = get_awards_html(i_awards)
    i_stat = df.loc[i, stat]
    tank_html_i = '|' + str(i + 1) + '|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) +\
        '"><span class="' + str(i_color) + '">' + str(i_name) + '</span>' + str(i_awards_html) + '</a>|' + str(i_stat) + '|\n'
    return(tank_html_i)

def get_html(df, stat = 'time_played'):
    tank_html = ''
    for i in range(len(df)):
        tank_html += get_html_i(df, i, stat)
    return(tank_html)

def get_md(f, df, table_id = 'stats_leaderboard_playtime', col_name = 'Time Played', stat = 'time_played'):
    f.write('{:.stats_leaderboard#' + table_id + '}\n')
    f.write('|<span class="num_col">&nbsp;</span>|<span class="tank_col">Tank</span>|<span class="stat_col">' + col_name + '</span>|\n')
    f.write(get_html(df, stat))
    f.write('\n\n')

#----- main

if __name__ == '__main__':
    # load and extract time
    all_tanks = pd.read_csv(all_tanks_csv)
    all_tanks = extract_time(all_tanks)
    last_updated_time = max(pd.to_datetime(all_tanks['time_now']))
    # dfs
    deaths = all_tanks.sort_values('deactivated', ascending = False).reset_index(drop = True).head(pop_stats_overall_max_display)
    deaths = deaths[deaths['deactivated'] != 0].reset_index(drop = True)
    kills = all_tanks.sort_values('destroyed_enemies', ascending = False).reset_index(drop = True).head(pop_stats_overall_max_display)
    kills = kills[kills['destroyed_enemies'] != 0].reset_index(drop = True)
    playtime = all_tanks.sort_values('total_seconds', ascending = False).reset_index(drop = True).head(pop_stats_overall_max_display)
    playtime = playtime[playtime['total_seconds'] != 0].reset_index(drop = True)
    # pop
    with open(pop_stats_overall_md, 'w') as f:
        f.write('\n## Overall Stats Leaderboard\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/">Top 100</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t100-overall-passes">Passes</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-overall">Stats Leaderboard</a></p>\n\n')
        f.write('<p class="stats_leaderboard"><a onclick="searchPlaytime();">Time Played</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a onclick="searchKills();">Kills</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a onclick="searchDeaths();">Deaths</a></p>\n\n')
        get_md(f, playtime, 'stats_leaderboard_playtime', 'Time Played', 'time_played')
        get_md(f, kills, 'stats_leaderboard_kills', 'Kills', 'destroyed_enemies')
        get_md(f, deaths, 'stats_leaderboard_deaths', 'Deaths', 'deactivated')
        f.write('\n\n' + get_last_updated_html('Last Updated', last_updated_time))
