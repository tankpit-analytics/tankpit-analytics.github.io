dir_tpdata = '/Users/thomas/Desktop/tpdata/'
dir_git    = '/Users/thomas/git/tankpit-analytics.github.io/'
path_check =  dir_tpdata + 'check/is_5m_job_running.csv'

api_delay = 1
api_max_tries = 40

#========== data

#-----t100 overall

master_csv_overall = dir_tpdata + 'master_overall.csv'
passes_csv_overall = dir_tpdata + 'passes_overall.csv'

# 2020-07-12
# ~ <283 accurate
# !--gen4 231
# !--gen5 276
# gen6 332
# col2 306
# maj2 283
# !--cap1 189
# cap2 ?
# lieut1 388

# 2020-09-13
# 6 +2 gen= 8
# 2 +2 col= 4
# 2 +2 maj= 4
# 2 +1 cap= 3
# 1 +1 lie= 2

# 2020-09-15
# 8 +4 gen= 12
# 4 +4 col= 8
# 4 +4 maj= 8
# 3 +3 cap= 6
# 2 +2 lie= 4

# look back in about a week or so and cut it down...

ranks_dict_overall = {
    'general': 12,
    'colonel': 8,
    'major': 8,
    'captain': 6,
    'lieutenant': 4
}

# ranks_dict_overall = {
#     'general': 4,
#     'colonel': 2,
#     'major': 2,
#     'captain': 1,
#     'lieutenant': 1,
#     'sergeant': 1,
#     'corporal': 1,
#     'private': 1,
#     'recruit': 1
# }

master_nrow_overall = 600 # rows in master - if running j loop, increasing this takes a lot longer

#-----t100 2020

master_csv_2020 = dir_tpdata + 'master_2020.csv'
passes_csv_2020 = dir_tpdata + 'passes_2020.csv'

# 2020-07-12
# ~ <171 accurate
# gen2 180
# col2 171
# maj2 234
# cap1 210
# lie1 248

ranks_dict_2020 = {
    'general': 2,
    'colonel': 2,
    'major': 2,
    'captain': 1,
    'lieutenant': 1
}

# ranks_dict_2020 = {
#     'general': 4,
#     'colonel': 2,
#     'major': 2,
#     'captain': 1,
#     'lieutenant': 1,
#     'sergeant': 1,
#     'corporal': 1,
#     'private': 1,
#     'recruit': 1
# }

master_nrow_2020 = 500 # rows in master - if running j loop, increasing this takes a lot longer

#-----get all tanks
#requires: ranks_dict_overall

all_tanks_csv = dir_tpdata + 'all_tanks.csv'

#-----get all tanks stats
#requires: all_tanks_csv, awards_dict

full_loop_verbose = False
cup_counts_csv_1 = dir_tpdata + 'cup_counts_with_dupes.csv'
cup_counts_csv_2 = dir_tpdata + 'cup_counts.csv'

#----get 2020 tanks
#requires: ranks_dict_2020

y2020_tanks_csv = dir_tpdata + 'y2020_tanks.csv'

#-----get 2020 tanks stats
#requires: y2020_tanks_csv, awards_dict

all_tanks_csv_backup_prefix = dir_tpdata + 'backups/all_tanks_'

#-----get active

active_csv = dir_tpdata + 'active.csv'

#-----get upcoming tourn

upcoming_tourn_csv = dir_tpdata + 'upcoming_tourn.csv'

#========== populate

#-----pop t100
#requires: master_csv_overall, passes_csv_overall

pop_t_overall_rows = 100
pop_t_overall_md = dir_git + 'index.md'

#-----pop t100 passes
#requires: master_csv_overall, passes_csv_overall, pop_t_overall_rows

pop_t_overall_passes_max_display = 200
pop_t_overall_passes_md = dir_git + 't100-overall-passes.md'

#-----pop t25 2020
#requires: master_csv_2020, passes_csv_2020

pop_t_2020_rows = 25
pop_t_2020_md = dir_git + 't25-2020.md'

#-----pop t25 2020 passes
#requires: master_csv_2020, passes_csv_2020

pop_t_2020_passes_max_display = 1000
pop_t_2020_passes_md = dir_git + 't25-2020-passes.md'

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

pop_awards_search_md = dir_git + 'awards-search.md'

#-----pop cups leaderboard
#requires: cup_counts_csv_2

pop_cups_leaderboard_max_display = 25
pop_cups_leaderboard_md = dir_git + 'cups-leaderboard.md'

#-----pop stats overall
#requires: all_tanks_csv

pop_stats_overall_max_display = 100
pop_stats_overall_md = dir_git + 'stats-overall.md'

#-----pop stats 2020
#requires: y2020_tanks_csv

pop_stats_2020_max_display = 100
pop_stats_2020_md = dir_git + 'stats-2020.md'

#-----pop 130k club

# note: for now, only 1 tank per person... maybe keep track of this and add a new feature over time to have multiples per person
tourn_130k_club_dict = {
    9389:  [{'tourn_id': 168,  'cup': 'silver'}], #kacy
    11644: [{'tourn_id': 888,  'cup': 'gold'}], #jay
    70106: [{'tourn_id': 1062, 'cup': 'gold'}], #adam
    30661: [{'tourn_id': 1242, 'cup': 'silver'}], #, {'tourn_id': 1372, 'cup': 'bronze'}], #tm2
    827:   [{'tourn_id': 1712, 'cup': 'bronze'}] #lefty
}

tourn_130k_club_csv = dir_tpdata + 'tourn_130k_club.csv'
pop_tourn_130k_club_md = dir_git + '130k-club.md'
