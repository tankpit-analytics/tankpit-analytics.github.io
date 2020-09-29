from pop_t100_overall import *

#---- helpers

def get_md(awards_dict, full_awards_dict, all_tanks, f):
    for award in awards_dict.keys():
        for award_tier in [1,2,3]:
            y = all_tanks['awards'].apply(lambda x: has_award(x, awards_dict, award, award_tier))
            award_df = all_tanks[y].reset_index(drop = True)
            award_count = award_df.shape[0]
            if award_count != 0:
                award_df = rank_by_awards(award_df, awards_dict)
                full_award_name = full_awards_dict[str(award) + str(award_tier)]
                f.write('<span class="awards_search_header" id="awards_search_header_' + str(award) + str(award_tier) + '">' + str(full_award_name) + ' (' + str(award_count) + ')</span>\n\n')
                f.write('{:.awards_search#awards_search_' + str(award) + str(award_tier) + '}\n')
                f.write(get_tank_html(award_df))
                f.write('\n\n')

#----- main

if __name__ == '__main__':
    all_tanks = pd.read_csv(all_tanks_csv)
    all_tanks = all_tanks.sort_values('id', ascending = True).reset_index(drop = True)
    last_updated_time = max(pd.to_datetime(all_tanks['time_now']))
    # pop
    with open(pop_awards_search_md, 'w') as f:
        f.write('\n## Awards Search\n\n')
        f.write('<p><a href="https://tankpit-analytics.github.io/awards-search">Awards Search</a>&nbsp;&nbsp;|&nbsp;&nbsp;<a href="https://tankpit-analytics.github.io/latest-sword-decorations">Latest Sword Decorations</a></p>\n\n')
        f.write('{:.awards_search_selection}\n')
        f.write('|<a onclick="searchStar1();"><span class="awards-sprite a0-1"></span></a>|<a onclick="searchTank1();"><span class="awards-sprite a1-1"></span></a>|<a onclick="searchMedal1();"><span class="awards-sprite a2-1"></span></a>|<a onclick="searchSword1();"><span class="awards-sprite a3-1"></span></a>|<a onclick="searchDoT();"><span class="awards-sprite a4-3"></span></a>|<a onclick="searchCup1();"><span class="awards-sprite a5-1"></span></a>|<a onclick="searchPH();"><span class="awards-sprite a6-1"></span></a>|<a onclick="searchWC();"><span class="awards-sprite a7-1"></span></a>|<a onclick="searchLB();"><span class="awards-sprite a8-1"></span></a>|\n')
        f.write('|<a onclick="searchStar2();"><span class="awards-sprite a0-2"></span></a>|<a onclick="searchTank2();"><span class="awards-sprite a1-2"></span></a>|<a onclick="searchMedal2();"><span class="awards-sprite a2-2"></span></a>|<a onclick="searchSword2();"><span class="awards-sprite a3-2"></span></a>|<a onclick="searchDoT();"><span class="awards-sprite a4-3"></span></a>|<a onclick="searchCup2();"><span class="awards-sprite a5-2"></span></a>|<a onclick="searchPH();"><span class="awards-sprite a6-1"></span></a>|<a onclick="searchWC();"><span class="awards-sprite a7-1"></span></a>|<a onclick="searchLB();"><span class="awards-sprite a8-1"></span></a>|\n')
        f.write('|<a onclick="searchStar3();"><span class="awards-sprite a0-3"></span></a>|<a onclick="searchTank3();"><span class="awards-sprite a1-3"></span></a>|<a onclick="searchMedal3();"><span class="awards-sprite a2-3"></span></a>|<a onclick="searchSword3();"><span class="awards-sprite a3-3"></span></a>|<a onclick="searchDoT();"><span class="awards-sprite a4-3"></span></a>|<a onclick="searchCup3();"><span class="awards-sprite a5-3"></span></a>|<a onclick="searchPH();"><span class="awards-sprite a6-1"></span></a>|<a onclick="searchWC();"><span class="awards-sprite a7-1"></span></a>|<a onclick="searchLB();"><span class="awards-sprite a8-1"></span></a>|\n\n')
        get_md(awards_dict, full_awards_dict, all_tanks, f)
        f.write('\n\n' + get_last_updated_html('Last Updated', last_updated_time))
