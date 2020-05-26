# ===== INSERT CHANNEL WEBHOOK HERE

CHANNEL_WEBHOOK_URL = 'https://discordapp.com/api/webhooks/_____________________________________'

# ===================================
# ===================================

import time
import requests
import numpy as np
from datetime import datetime
from pytz import timezone

# ===== API

api_delay = 1
api_max_tries = 10

# -----

def make_code(string):
    return('```' + string + '```')

def add_delay(seconds = api_delay):
    time.sleep(seconds)

def get_request(link):
    add_delay()
    response = requests.get(link)
    return(response)

def get_dict_from_url(link, max_tries = api_max_tries):
    for tries in range(1, max_tries + 1):
        response = get_request(link)
        # if success, break
        if response.status_code == 200:
            break
        # otherwise, print error and re-try
        print(tries, 'GET request error (' + str(response.status_code) + '), trying again for:', link, str(datetime.now()))
    response_dict = response.json()
    return(response_dict)

def get_tourney_dict():
    tourn_dict = get_dict_from_url('https://tankpit.com/api/upcoming_tournaments')
    tourn_dict = tourn_dict[0]
    start_time = datetime.strptime(tourn_dict['start_time_utc'], '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone('UTC'))
    end_time = datetime.strptime(tourn_dict['end_time_utc'], '%Y-%m-%d %H:%M:%S').replace(tzinfo = timezone('UTC'))
    tmap = tourn_dict['map']
    # duration
    duration_minutes, duration_seconds = divmod((end_time - start_time).total_seconds(), 60)
    duration_minutes = int(duration_minutes)
    duration_seconds = int(duration_seconds)
    duration_hours = int(duration_minutes / 60)
    if (duration_minutes != 60) | (duration_seconds != 0):
        duration_hours = duration_minutes / 60
    # time until
    time_now = datetime.utcnow().replace(tzinfo = timezone('UTC'))
    hours_til, seconds_til = divmod((start_time - time_now).total_seconds(), 3600)
    days_til = int(np.floor(hours_til / 24))
    hours_til = int(np.floor(hours_til - (days_til * 24)))
    minutes_til = int(np.floor(seconds_til / 60))
    # tz
    start_time_pacific = start_time.astimezone(timezone('US/Pacific')).strftime("%A, %B %d, %-I:%M %p")
    start_time_eastern = start_time.astimezone(timezone('US/Eastern')).strftime("%A, %B %d, %-I:%M %p")
    start_time_brisbane = start_time.astimezone(timezone('Australia/Brisbane')).strftime("%A, %B %d, %-I:%M %p")
    start_time_singapore = start_time.astimezone(timezone('Singapore')).strftime("%A, %B %d, %-I:%M %p")
    start_time_london = start_time.astimezone(timezone('Europe/London')).strftime("%A, %B %d, %-I:%M %p")
    return({
        'duration_hours': duration_hours,
        'days_til': days_til,
        'hours_til': hours_til,
        'minutes_til': minutes_til,
        'start_time_pacific': start_time_pacific,
        'start_time_eastern': start_time_eastern,
        'start_time_london': start_time_london,
        'start_time_singapore': start_time_singapore,
        'start_time_brisbane': start_time_brisbane,
        'tmap': tmap
    })

def get_tourney():
    tourney_dict = get_tourney_dict()
    # hours
    hours_suffix = 'hours'
    if tourney_dict['hours_til'] == 1:
        hours_suffix = 'hour'
    duration_hours_suffix = 'hours'
    if tourney_dict['duration_hours'] == 1:
        duration_hours_suffix = 'hour'
    # string
    tourney_string = 'Next tournament in:  ' +\
        str(tourney_dict['days_til']) + ' day, ' + str(tourney_dict['hours_til']) + ' ' +\
        hours_suffix + ', ' + str(tourney_dict['minutes_til']) + ' minutes\n' +\
        '               Map:  ' + tourney_dict['tmap'] + '\n'\
        '          Duration:  ' + str(tourney_dict['duration_hours']) + ' ' + duration_hours_suffix + '\n'
    return(make_code(tourney_string))

# ===== DISCORD ALERTS

if __name__ == '__main__':
    while True:
        tourn_dict = get_tourney_dict()
        tourn_alert = '@here Tournament soon!  Get ready for battle!' + get_tourney()
        # sends an alert to channel when tourney is 5 minutes away
        if (tourn_dict['days_til'] == 0) & (tourn_dict['hours_til'] == 0) & (tourn_dict['minutes_til'] == 5):
            requests.post(CHANNEL_WEBHOOK_URL, data = {'content': tourn_alert})
        add_delay(45) # 45 second delay to check again
