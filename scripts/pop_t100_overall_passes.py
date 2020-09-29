from helper import *

#---- helpers

def action_is_pass(action_str):
    is_pass = False
    if action_str.find('pass (') != -1:
        is_pass = True
    return(is_pass)

def edit_passed_rank(new_row):
    new_row += 1
    if int(new_row) <= 25:
        new_row_str = '<span class="green">' + str(new_row) + '</span>'
    elif int(new_row) <= 50:
        new_row_str = '<span class="orange">' + str(new_row) + '</span>'
    else:
        new_row_str = '<span class="red">' + str(new_row) + '</span>'
    return(new_row_str)

def clean_passes_df(passes_df, max_rank):
    # reverse sort
    passes_df = passes_df.sort_index(ascending = False)
    # only keep passes
    passes_df['is_pass'] = passes_df['action'].apply(lambda x: action_is_pass(x))
    passes_df = passes_df[passes_df['is_pass']]
    # only keep passes under a certain number (new_row == 0 is lowest for number 1)
    passes_df = passes_df[passes_df['new_row'].astype(str).str.len() < 4] # cleaning up this col
    passes_df['new_row'] = passes_df['new_row'].fillna(-1)
    passes_df['new_row'] = passes_df['new_row'].astype(float).astype(int)
    passes_df = passes_df[(passes_df['new_row'] >= 0) & (passes_df['new_row'] < max_rank)]
    passes_df['new_row'] = passes_df['new_row'].apply(lambda x: edit_passed_rank(x))
    # cleaning
    passes_df['passed_tank_id'] = passes_df['passed_tank_id'].astype(int)
    passes_df = passes_df.drop('is_pass', axis = 1)
    passes_df['new_time'] = pd.to_datetime(passes_df['time']).dt.strftime("%b %-d: %-I:%M %p")#.strftime("%b %d, %Y: %-I:%M %p")
    passes_df['month'] = pd.to_datetime(passes_df['time']).dt.strftime("%B %Y")
    return(passes_df.reset_index(drop = True))

def get_html_i(passes_df, tank_dict, i, has_date_col = False):
    i_time = passes_df.loc[i, 'new_time']
    i_id = passes_df.loc[i, 'tank_id']
    i_name = tank_dict[i_id]['name']
    i_color = tank_dict[i_id]['color']
    i_awards_html = get_awards_html(tank_dict[i_id]['awards'])
    i_passed_id = passes_df.loc[i, 'passed_tank_id']
    i_passed_name = tank_dict[i_passed_id]['name']
    i_passed_color = tank_dict[i_passed_id]['color']
    i_passed_awards_html = get_awards_html(tank_dict[i_passed_id]['awards'])
    i_n = passes_df.loc[i, 'new_row']
    html_i = ''
    if has_date_col:
        html_i = html_i + '|' + str(i_time)
    html_i = html_i + '|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) + '"><span class="' +\
        str(i_color) + '">' + str(i_name) + '</span>' + str(i_awards_html) +\
        '</a>|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' +\
        str(i_passed_id) + '"><span class="' + str(i_passed_color) + '">' + str(i_passed_name) + '</span>' +\
        str(i_passed_awards_html) + '</a>|' + str(i_n) + '|\n'
    return(html_i)

def get_html(passes_df, tank_dict, has_date_col = False):
    html = ''
    for i in range(len(passes_df)):
        html += get_html_i(passes_df, tank_dict, i, has_date_col)
    return(html)

def get_md(passes_df, tank_dict, f, include_last_month = True):
    months = passes_df['month'].unique()
    if not include_last_month:
        months = months[:-1]
    for month in months:
        tmp_df = passes_df[passes_df['month'] == month].reset_index(drop = True)
        f.write('<span class="t100_month">' + str(month) + '</span>\n\n')
        # desktop
        f.write('{:.t100_passes.t100_passes_desktop}\n')
        f.write('|<span class="t100_date">Date</span>|<span class="tank_col">Tank</span>|<span class="tank_col">Passed</span>|<span class="t100_rank">#</span>|\n')
        f.write(get_html(tmp_df, tank_dict, True))
        f.write('\n')
        # mobile
        f.write('{:.t100_passes.t100_passes_mobile}\n')
        f.write('|<span class="tank_col">Tank</span>|<span class="tank_col">Passed</span>|<span class="t100_rank">#</span>|\n')
        f.write(get_html(tmp_df, tank_dict, False))
        f.write('\n\n')

#----- main

if __name__ == '__main__':
    # load and clean
    master_df = pd.read_csv(master_csv_overall)
    passes_df = pd.read_csv(passes_csv_overall)
    passes_df = clean_passes_df(passes_df, pop_t_overall_rows)
    passes_df = passes_df.head(pop_t_overall_passes_max_display)
    # get
    unique_master_tank_id_list = list(master_df['id'])
    unique_tank_id_list = list(set(list(passes_df['tank_id']) + list(passes_df['passed_tank_id'])))
    get_tank_id_list = [i for i in unique_tank_id_list if i not in unique_master_tank_id_list]
    unique_tank_dict = {}
    for tank_id in get_tank_id_list:
        unique_tank_dict[tank_id] = get_tank_stats(tank_id)
    # have
    have_tank_id_list = [i for i in unique_tank_id_list if i not in get_tank_id_list]
    for tank_id in have_tank_id_list:
        unique_tank_dict[tank_id] = get_tank_stats_from_master_df(master_df, tank_id)
    # pop
    with open(pop_t_overall_passes_md, 'w') as f:
        f.write('\n## Overall Top 100 - Passes\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/">Top 100</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/t100-overall-passes">Passes</a>&nbsp;&nbsp;|&nbsp;&nbsp;' + \
            '<a href="https://tankpit-analytics.github.io/stats-overall">Stats Leaderboard</a></p>\n\n')
        get_md(passes_df, unique_tank_dict, f, False)
        f.write('\n\n' + get_last_updated_html('Last Updated', time_now, time_now = True))
