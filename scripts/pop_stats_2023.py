from pop_stats_overall import *

#----- main

if __name__ == '__main__':
    # load and extract time
    y2023_tanks = pd.read_csv(y2023_tanks_csv)
    y2023_tanks = extract_time(y2023_tanks)
    last_updated_time = max(pd.to_datetime(y2023_tanks['time_now']))
    # dfs
    deaths = y2023_tanks.sort_values('deactivated', ascending = False).reset_index(drop = True).head(pop_stats_overall_max_display)
    deaths = deaths[deaths['deactivated'] != 0].reset_index(drop = True)
    kills = y2023_tanks.sort_values('destroyed_enemies', ascending = False).reset_index(drop = True).head(pop_stats_overall_max_display)
    kills = kills[kills['destroyed_enemies'] != 0].reset_index(drop = True)
    playtime = y2023_tanks.sort_values('total_seconds', ascending = False).reset_index(drop = True).head(pop_stats_overall_max_display)
    playtime = playtime[playtime['total_seconds'] != 0].reset_index(drop = True)
    # pop
    with open(pop_stats_2023_md, 'w') as f:
        f.write('\n## 2023 Stats Leaderboard\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/t25-2023">Top 25</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t25-2023-passes">Passes</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-2023">Stats Leaderboard</a></p>\n\n')
        f.write('<p class="stats_leaderboard"><a onclick="searchPlaytime();">Time Played</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a onclick="searchKills();">Kills</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a onclick="searchDeaths();">Deaths</a></p>\n\n')
        get_md(f, playtime, 'stats_leaderboard_playtime', 'Time Played', 'time_played')
        get_md(f, kills, 'stats_leaderboard_kills', 'Kills', 'destroyed_enemies')
        get_md(f, deaths, 'stats_leaderboard_deaths', 'Deaths', 'deactivated')
        f.write('\n\n' + get_last_updated_html('Last Updated', last_updated_time))
