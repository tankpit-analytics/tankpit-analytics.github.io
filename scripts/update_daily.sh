# full stats loop: 3h 31mins
# skip no awards in full stats loop (current): 1hr 9mins
# ^outdated

SCRIPTSDIR=/Users/thomas/git/tankpit-analytics.github.io/scripts
DATADIR=/Users/thomas/Desktop/tpdata
LOGDIR=/Users/thomas/Desktop/tpdata/log
PYTHON=/anaconda3/bin/python
STDLOG=$LOGDIR/update_daily.log
STDERR=$LOGDIR/update_daily.err
STDOUT=$LOGDIR/update_daily.out

# log
echo "#\nJob started: " $(date) >> $STDLOG
echo "#\nJob started: " $(date) >> $STDERR
echo "#\nJob started: " $(date) >> $STDOUT

# creds
source ~/.bash_profile

# pull
cd $SCRIPTSDIR
git reset --hard
git pull

# populate t100 (last updated: time_now)
$PYTHON $SCRIPTSDIR/pop_t100_overall.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_t25_2022.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_t100_overall_passes.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_t25_2022_passes.py >> $STDLOG 2>&1

# push
git add .
git commit -a -m "Automated daily commit triggered (1 of 2)."
git push origin master

# data - for each daily data job, make sure to add skip_mins param to any API query
#$PYTHON $SCRIPTSDIR/get_roster_col.py >> $LOGDIR/get_roster_col.log 2>&1 # 2022-specific
$PYTHON $SCRIPTSDIR/get_130k_club.py >> $LOGDIR/get_130k_club.log 2>&1 # 16 sec
$PYTHON $SCRIPTSDIR/get_2022_tanks.py >> $LOGDIR/get_2022_tanks.log 2>&1 # 47 sec
$PYTHON $SCRIPTSDIR/get_all_tanks.py >> $LOGDIR/get_all_tanks.log 2>&1 # 35 min
$PYTHON $SCRIPTSDIR/get_2022_tanks_stats.py >> $LOGDIR/get_2022_tanks_stats.log 2>&1 # 3 min
$PYTHON $SCRIPTSDIR/get_all_tanks_stats.py >> $LOGDIR/get_all_tanks_stats.log 2>&1 # 2.5 hr
$PYTHON $SCRIPTSDIR/get_sword_decorations.py >> $LOGDIR/get_sword_decorations.log 2>&1 # no API; after get_all_tanks_stats

# populate the rest (last updated: all_tanks.csv / 2022_tanks.csv - above "data")
$PYTHON $SCRIPTSDIR/pop_130k_club.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_awards_search.py >> $STDLOG 2>&1
#$PYTHON $SCRIPTSDIR/pop_cups_leaderboard.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_stats_overall.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_stats_2022.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_sword_decorations.py >> $STDLOG 2>&1

# push
git add .
git commit -a -m "Automated daily commit triggered (2 of 2)."
git push origin master

# log
echo "Job ended: " $(date) >> $STDLOG
echo "Job ended: " $(date) >> $STDERR
echo "Job ended: " $(date) >> $STDOUT
