#========== data

#-----t100 overall

master_csv_overall = '/Users/thomas/Desktop/tpdata/master_overall.csv'
passes_csv_overall = '/Users/thomas/Desktop/tpdata/passes_overall.csv'

ranks_dict_overall = {
    'general': 8,
    'colonel': 3,
    'major': 3,
    'captain': 1,
    'lieutenant': 1,
    'sergeant': 1,
    'corporal': 1,
    'private': 1,
    'recruit': 1
}

master_nrow_overall = 500 # rows in master - if running j loop, increasing this takes a lot longer

#-----t100 2020

master_csv_2020 = '/Users/thomas/Desktop/tpdata/master_2020.csv'
passes_csv_2020 = '/Users/thomas/Desktop/tpdata/passes_2020.csv'

ranks_dict_2020 = {
    'general': 4,
    'colonel': 3,
    'major': 3,
    'captain': 2,
    'lieutenant': 2,
    'sergeant': 1,
    'corporal': 1,
    'private': 1,
    'recruit': 1
}

master_nrow_2020 = 500 # rows in master - if running j loop, increasing this takes a lot longer

#-----get all tanks
#requires: ranks_dict_overall

all_tanks_csv = '/Users/thomas/Desktop/tpdata/all_tanks.csv'

#-----get all tanks stats
#requires: all_tanks_csv, awards_dict

cup_counts_csv_1 = '/Users/thomas/Desktop/tpdata/cup_counts_with_dupes.csv'
cup_counts_csv_2 = '/Users/thomas/Desktop/tpdata/cup_counts.csv'

#----get 2020 tanks
#requires: ranks_dict_2020

y2020_tanks_csv = '/Users/thomas/Desktop/tpdata/y2020_tanks.csv'

#-----get 2020 tanks stats
#requires: y2020_tanks_csv, awards_dict

#-----get active

active_csv = '/Users/thomas/Desktop/tpdata/active.csv'

#========== populate

#-----pop t100
#requires: master_csv_overall, passes_csv_overall

pop_t_overall_rows = 100
pop_t_overall_md = '/Users/thomas/git/tankpit-analytics.github.io/index.md'

#-----pop t100 passes
#requires: master_csv_overall, passes_csv_overall, pop_t_overall_rows

pop_t_overall_passes_max_display = 200
pop_t_overall_passes_md = '/Users/thomas/git/tankpit-analytics.github.io/t100-overall-passes.md'

#-----pop t25 2020
#requires: master_csv_2020, passes_csv_2020

pop_t_2020_rows = 25
pop_t_2020_md = '/Users/thomas/git/tankpit-analytics.github.io/t25-2020.md'

#-----pop t25 2020 passes
#requires: master_csv_2020, passes_csv_2020

pop_t_2020_passes_max_display = 1000
pop_t_2020_passes_md = '/Users/thomas/git/tankpit-analytics.github.io/t25-2020-passes.md'

#-----pop awards search
#requires: all_tanks_csv

awards_dict = {
    'star': 0,
    'tank': 1,
    'medal': 2,
    'sword': 3,
    'dot': 4,
    'cup': 5,
    'ph': 6,
    'wc': 7,
    'lb': 8
}

full_awards_dict = {
    'star1': 'Single Star',
    'star2': 'Double Star',
    'star3': 'Triple Star',
    'tank1': 'Bronze Tank',
    'tank2': 'Silver Tank',
    'tank3': 'Golden Tank',
    'medal1': 'Combat Honor Medal',
    'medal2': 'Battle Honor Medal',
    'medal3': 'Heroic Honor Medal',
    'sword1': 'Shining Sword',
    'sword2': 'Battered Sword',
    'sword3': 'Rusty Sword',
    'cup1': 'Bronze Cup',
    'cup2': 'Silver Cup',
    'cup3': 'Gold Cup',
    'dot3': 'Defender of the Truth',
    'ph1': 'Purple Heart',
    'wc1': 'War Correspondent',
    'lb1': 'Lightbulb'
}

pop_awards_search_md = '/Users/thomas/git/tankpit-analytics.github.io/awards-search.md'

#-----pop cups leaderboard
#requires: cup_counts_csv_2

pop_cups_leaderboard_max_display = 25
pop_cups_leaderboard_md = '/Users/thomas/git/tankpit-analytics.github.io/cups-leaderboard.md'

#-----pop stats overall
#requires: all_tanks_csv

pop_stats_overall_max_display = 100
pop_stats_overall_md = '/Users/thomas/git/tankpit-analytics.github.io/stats-overall.md'

#-----pop stats 2020
#requires: y2020_tanks_csv

pop_stats_2020_max_display = 100
pop_stats_2020_md = '/Users/thomas/git/tankpit-analytics.github.io/stats-2020.md'
