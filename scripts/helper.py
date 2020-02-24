from params import *

import pandas as pd
import time
import requests
from datetime import datetime

time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Pacific if run on my machine

#----- API

def add_delay(seconds = api_delay):
    time.sleep(seconds)

def get_request(link):
    add_delay()
    response = requests.get(link)
    return(response)

# this is the main fxn that contains the delays + skip_mins for multiple simultaneous jobs
def get_dict_from_url(link, skip_mins = False, max_tries = api_max_tries):
    for tries in range(1, max_tries + 1):
        # daily job
        if skip_mins == True:
            minute_now = int(datetime.now().minute)
            cond_1 = (minute_now >= 0) & (minute_now < 2)
            cond_2 = (minute_now >= 15) & (minute_now < 17)
            cond_3 = (minute_now >= 30) & (minute_now < 32)
            cond_4 = (minute_now >= 45) & (minute_now < 47)
            if cond_1 | cond_2 | cond_3 | cond_4:
                # don't run
                add_delay(15)
            else:
                # run!
                response = get_request(link)
                if response.status_code == 200:
                    break
                print(tries, '[min: ' + str(minute_now) + '] GET request error (' + str(response.status_code) + '), trying again for:', link)
        # 5min job
        else:
            response = get_request(link)
            if response.status_code == 200:
                break
            print(tries, '[min: ' + str(minute_now) + '] GET request error (' + str(response.status_code) + '), trying again for:', link)
    response_dict = response.json()
    return(response_dict)

def get_tank_dict(tank_id):
    return(get_dict_from_url('https://tankpit.com/api/tank?tank_id=' + str(tank_id)))

def get_tank_dict_leaderboard(tank_name):
    return(get_dict_from_url('https://tankpit.com/api/leaderboards/?leaderboard=overall&search=%22' + str(tank_name) + '%22'))

def get_tank_stats(tank_id):
    tank_dict = get_tank_dict(tank_id)
    tank_name = tank_dict['name']
    tank_awards = tank_dict['awards']
    try:
        tank_color = tank_dict['main_color']
    except:
        tank_list = get_tank_dict_leaderboard(tank_name)
        tank_dict_leaderboard = [i for i in tank_list['results'] if tank_id == i['tank_id']][0]
        tank_color = tank_dict_leaderboard['color']
    return({'name': tank_name,
            'color': tank_color,
            'awards': tank_awards})

#----- pd

def get_tank_stats_from_master_df(master_df, tank_id):
    tank_name = str(list(master_df.loc[master_df['id'] == tank_id, 'name'])[0])
    tank_color = str(list(master_df.loc[master_df['id'] == tank_id, 'color'])[0])
    tank_awards = str(list(master_df.loc[master_df['id'] == tank_id, 'awards'])[0])
    return({'name': tank_name,
            'color': tank_color,
            'awards': tank_awards})

def has_award(awards_str, awards_dict, award = 'star', award_tier = 0):
    tank_has_award = False
    # convert from string to list
    awards_list = str(awards_str).strip('][').split(', ')
    # make int
    awards_list = [int(i) for i in awards_list]
    if awards_list[awards_dict[award]] == award_tier:
        tank_has_award = True
    return(tank_has_award)

def has_award_01_notier(awards_str, awards_dict, award = 'star'):
    tank_has_award = 0
    # convert from string to list
    awards_list = str(awards_str).strip('][').split(', ')
    # make int
    awards_list = [int(i) for i in awards_list]
    if awards_list[awards_dict[award]] > 0:
        tank_has_award = 1
    return(tank_has_award)

def extract_award_value(awards_str, awards_dict, award = 'star'):
    # convert from string to list
    awards_list = str(awards_str).strip('][').split(', ')
    # make int
    awards_list = [int(i) for i in awards_list]
    return(awards_list[awards_dict[award]])

# number of awards -> sword -> id
def rank_by_awards(df, awards_dict):
    orig_cols = df.columns.copy()
    df['ph'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'ph'))
    df['wc'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'wc'))
    df['lb'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'lb'))
    df['dot'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'dot'))
    df['star'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'star'))
    df['tank'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'tank'))
    df['medal'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'medal'))
    df['sword'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'sword'))
    df['cup'] = df['awards'].apply(lambda x: has_award_01_notier(x, awards_dict, 'cup'))
    df['award_count'] = df[['ph','wc','lb','dot','star','tank','medal','sword','cup']].T.sum()
    df['sword_tier'] = df['awards'].apply(lambda x: extract_award_value(x, awards_dict, 'sword'))
    df['star_tier'] = df['awards'].apply(lambda x: extract_award_value(x, awards_dict, 'star'))
    df = df.sort_values(['award_count', 'sword_tier', 'star_tier', 'id'], ascending = [False, False, False, True])
    df.reset_index(drop = True, inplace = True)
    df = df[orig_cols]
    return(df)

def has_any_award(awards_str, awards_dict):
    has_award = False
    # convert from string to list
    awards_list = str(awards_str).strip('][').split(', ') 
    # make int
    awards_list = [int(i) for i in awards_list]
    if sum(awards_list) != 0:
        has_award = True
    return(has_award)

def has_one_award(awards_str, awards_dict):
    has_1_award = False
    # convert from string to list
    awards_list = str(awards_str).strip('][').split(', ') 
    # make int
    awards_list = [1 for i in awards_list if int(i) > 0]
    if sum(awards_list) == 1:
        has_1_award = True
    return(has_1_award)

def only_keep_has_any_award(df, awards_dict):
    df['has_any_award'] = df['awards'].apply(lambda x: has_any_award(x, awards_dict))
    df = df[df['has_any_award']].reset_index(drop = True)
    df = df.drop('has_any_award', axis = 1)
    return(df)

def remove_certain_single_awards(df, awards_dict):
    z = df['awards'].apply(lambda x: has_one_award(x, awards_dict))
    y1 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'star', 1)) & z
    y2 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'star', 2)) & z
    y3 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'star', 3)) & z
    y4 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'tank', 1)) & z
    y5 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'tank', 2)) & z
    y6 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'medal', 1)) & z
    df = df[~y1&~y2&~y3&~y4&~y5&~y6].reset_index(drop = True)
    return(df)

# ended up never using this
def keep_only_has_cup(df, awards_dict):
    y1 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'cup', 1))
    y2 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'cup', 2))
    y3 = df['awards'].apply(lambda x: has_award(x, awards_dict, 'cup', 3))
    df = df[y1|y2|y3].reset_index(drop = True)
    return(df)

#----- HTML

def get_awards_html(awards_str):
    awards_list = str(awards_str).strip('][').split(', ')
    awards_html = ''
    for i in range(len(awards_list)):
        a = int(awards_list[i])
        if a != 0:
            awards_html += '<span class="awards-sprite a' + str(i) + '-' + str(a) + '"></span>'
    return('<span class="awards-container">' + awards_html + '</span>')

def get_last_updated_html(blurb, last_updated_time, time_now = False):
    if time_now:
        last_updated_time = datetime.strptime(last_updated_time, '%Y-%m-%d %H:%M:%S')
    return('<p class="last_updated"><span class="last_updated">' + blurb + ':&nbsp;&nbsp;' +\
     last_updated_time.strftime("%b %-d, %-I:%M %p") + '&nbsp;&nbsp;(Pacific)</span></p>\n\n')
