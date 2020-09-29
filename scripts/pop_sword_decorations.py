from helper import *

#----- helpers

def clean_master_award_decorations_df(df):
    df['month'] = pd.to_datetime(df['award_time']).dt.strftime("%B %Y")
    df['new_time'] = pd.to_datetime(df['award_time']).dt.strftime("%b %-d, %Y")
    df = df.sort_values('award_time', ascending = False)
    return(df)

def get_sword_decorations_df(master_award_decorations_df):
    sword_decorations_df = master_award_decorations_df[master_award_decorations_df['award'] == 'sword']
    sword_decorations_df = sword_decorations_df[sword_decorations_df['tier'] > 0].reset_index(drop = True)
    return(sword_decorations_df)

def remove_tanks_manually(df, remove_decorations_list):
    for _id in remove_decorations_list:
        df = df[df['tank_id'] != _id].reset_index(drop = True)
    return(df)

# add more if doing more than sword later...
def get_decoration_html(award, tier):
    decoration_html = ''
    if award == 'sword':
        decoration_html = decoration_html + '<span class="awards-sprite a3-' + str(tier) + '"></span>'
    return(decoration_html)

def get_html_i(sword_decorations, tank_dict, i):
    i_time = sword_decorations.loc[i, 'new_time']
    i_id = sword_decorations.loc[i, 'tank_id']
    i_name = tank_dict[i_id]['name']
    i_color = tank_dict[i_id]['color']
    i_awards_html = get_awards_html(tank_dict[i_id]['awards'])
    i_decoration = sword_decorations.loc[i, 'award']
    i_tier = sword_decorations.loc[i, 'tier']
    i_decoration_html = get_decoration_html(i_decoration, i_tier)
    html_i = '|' + str(i_time) + '|' + str(i_decoration_html) + '|<a target="_blank" href="https://tankpit.com/tank_profile/?tank_id=' + str(i_id) + '"><span class="' +\
        str(i_color) + '">' + str(i_name) + '</span>' + str(i_awards_html) + '</a>|\n'
    return(html_i)

def get_html(sword_decorations, tank_dict):
    html = ''
    for i in range(len(sword_decorations)):
        html += get_html_i(sword_decorations, tank_dict, i)
    return(html)

def get_md(sword_decorations, tank_dict, f):
    months = sword_decorations['month'].unique()
    for month in months:
        tmp_df = sword_decorations[sword_decorations['month'] == month].reset_index(drop = True)
        f.write('<span class="decorations_month">' + str(month) + '</span>\n\n')
        f.write('{:.decorations}\n')
        f.write('|<span class="decorations_date">Date</span>|<span class="decoration">&nbsp;</span>|<span class="tank_col">Tank</span>|\n')
        f.write(get_html(tmp_df, tank_dict))
        f.write('\n')

#----- main

if __name__ == '__main__':
    # load and clean
    master_award_decorations_df = pd.read_csv(master_award_decorations_csv)
    master_award_decorations_df = clean_master_award_decorations_df(master_award_decorations_df)
    # sword-specific start
    sword_decorations = get_sword_decorations_df(master_award_decorations_df)
    sword_decorations = remove_tanks_manually(sword_decorations, remove_sword_decorations_list)
    last_updated_time = max(pd.to_datetime(sword_decorations['award_time']))
    master_df = pd.read_csv(all_tanks_csv)
    # get
    unique_master_tank_id_list = list(master_df['id'])
    unique_tank_id_list = list(set(list(sword_decorations['tank_id'])))
    get_tank_id_list = [i for i in unique_tank_id_list if i not in unique_master_tank_id_list]
    unique_tank_dict = {}
    for tank_id in get_tank_id_list:
        unique_tank_dict[tank_id] = get_tank_stats(tank_id)
    # have
    have_tank_id_list = [i for i in unique_tank_id_list if i not in get_tank_id_list]
    for tank_id in have_tank_id_list:
        unique_tank_dict[tank_id] = get_tank_stats_from_master_df(master_df, tank_id)
    # pop
    with open(sword_decorations_md, 'w') as f:
        f.write('\n## Sword Decorations\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/awards-search">Awards Search</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="https://tankpit-analytics.github.io/latest-sword-decorations">Sword Decorations</a></p>\n\n')
        get_md(sword_decorations, unique_tank_dict, f)
        f.write('\n\n' + get_last_updated_html('Last Updated', last_updated_time))
