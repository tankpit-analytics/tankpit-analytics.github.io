dir_tpdata = '/Users/thomas/Desktop/tpdata/'
dir_git    = '/Users/thomas/git/tankpit-analytics.github.io/'
path_check =  dir_tpdata + 'check/is_5m_job_running.csv'

api_delay = 1
api_max_tries = 150

#========== data

#-----t100 overall params

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

# run gen= 20 once (500), then change to 8, follow below

# 2020-09-13
# 6 +2 gen= 8
# 2 +2 col= 4
# 2 +2 maj= 4
# 2 +1 cap= 3
# 1 +1 lie= 2

ranks_dict_overall = {
    'general': 8,
    'colonel': 3,
    'major': 3,
    'captain': 3,
    'lieutenant': 2
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

master_nrow_overall = 500 # rows in master - if running j loop, increasing this takes a lot longer

#-----t100 2020 params
#requires: master_csv_overall (if using supplement job)

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

#-----t100 2021 params
#requires: master_csv_overall (if using supplement job)

master_csv_2021 = dir_tpdata + 'master_2021.csv'
passes_csv_2021 = dir_tpdata + 'passes_2021.csv'

ranks_dict_2021 = {
    'general': 2,
    'colonel': 2,
    'major': 2,
    'captain': 1,
    'lieutenant': 1
}

master_nrow_2021 = 500 # rows in master - if running j loop, increasing this takes a lot longer

#-----backups

all_tanks_csv_backup_prefix = dir_tpdata + 'backups/all_tanks_'

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

#----get 2021 tanks
#requires: ranks_dict_2021

y2021_tanks_csv = dir_tpdata + 'y2021_tanks.csv'

#-----get 2021 tanks stats
#requires: y2021_tanks_csv, awards_dict

#-----get active

active_csv = dir_tpdata + 'active.csv'

#-----get upcoming tourn

upcoming_tourn_csv = dir_tpdata + 'upcoming_tourn.csv'

#-----get sword decorations

dir_backups = dir_tpdata + 'backups/'
done_filenames_list_pickle = dir_tpdata + 'done_filenames_list.pickle'
backups_concat_pickle = dir_tpdata + 'backups_concat.pickle'
master_award_decorations_csv = dir_tpdata + 'master_award_decorations.csv'

lookback_days = 30
# 7 days = 20 seconds
# 30 days = 27 seconds
# 365 days = 80 seconds

award_string_conversion = {
    1: 'star',
    4: 'tank',
    7: 'medal',
    10: 'sword',
    13: 'dot',
    16: 'cup',
    19: 'ph',
    22: 'wc',
    25: 'lb'
}

remove_sword_decorations_list = [
    71930 # john gotti (71930) - sword stripped?
]

#========== populate

#-----pop t100
#requires: master_csv_overall, passes_csv_overall

pop_t_overall_rows = 100
pop_t_overall_md = dir_git + 'index.md'

#-----pop t100 passes
#requires: master_csv_overall, passes_csv_overall, pop_t_overall_rows

pop_t_overall_passes_max_display = 500
pop_t_overall_passes_md = dir_git + 't100-overall-passes.md'

#-----pop t25 2020
#requires: master_csv_2020, passes_csv_2020

pop_t_2020_rows = 25
pop_t_2020_md = dir_git + 't25-2020.md'

#-----pop t25 2020 passes
#requires: master_csv_2020, passes_csv_2020

pop_t_2020_passes_max_display = 1000
pop_t_2020_passes_md = dir_git + 't25-2020-passes.md'

#-----pop t25 2021
#requires: master_csv_2021, passes_csv_2021

pop_t_2021_rows = 25
pop_t_2021_md = dir_git + 't25-2021.md'

#-----pop t25 2021 passes
#requires: master_csv_2021, passes_csv_2021

pop_t_2021_passes_max_display = 1000
pop_t_2021_passes_md = dir_git + 't25-2021-passes.md'

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

#-----pop stats 2021
#requires: y2021_tanks_csv

pop_stats_2021_max_display = 100
pop_stats_2021_md = dir_git + 'stats-2021.md'

#-----pop 130k club

# note: for now, only 1 tank per person... maybe keep track of this and add a new feature over time to have multiples per person
tourn_130k_club_dict = {
    9389:  [{'tourn_id': 168,  'cup': 'silver'}], #kacy
    11644: [{'tourn_id': 888,  'cup': 'gold'}], #jay
    70106: [{'tourn_id': 1062, 'cup': 'gold'}], #adam
    30661: [{'tourn_id': 1242, 'cup': 'silver'}], #, {'tourn_id': 1372, 'cup': 'bronze'}], #tm2
    827:   [{'tourn_id': 1712, 'cup': 'bronze'}], #lefty
    45863: [{'tourn_id': 1742, 'cup': 'silver'}], #me
    539: [{'tourn_id': 1857, 'cup': 'bronze'}], #bg
    34871: [{'tourn_id': 1883, 'cup': 'silver'}], #azn
    35146: [{'tourn_id': 1977, 'cup': 'bronze'}] #noodle
}

tourn_130k_club_csv = dir_tpdata + 'tourn_130k_club.csv'
pop_tourn_130k_club_md = dir_git + '130k-club.md'

#-----pop sword decorations
#requires: all_tanks_csv

# note: rename from 'latest-sword-decorations' -> 'sword-decorations' at a later time (this link is the only thing left)
sword_decorations_md = dir_git + 'latest-sword-decorations.md'
