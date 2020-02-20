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
$PYTHON $SCRIPTSDIR/pop_t25_2020.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_t100_overall_passes.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_t25_2020_passes.py >> $STDLOG 2>&1

# data
$PYTHON $SCRIPTSDIR/get_2020_tanks.py >> $LOGDIR/get_2020_tanks.log 2>&1 # 14 secs
$PYTHON $SCRIPTSDIR/get_all_tanks.py >> $LOGDIR/get_all_tanks.log 2>&1 # 14 mins
$PYTHON $SCRIPTSDIR/get_2020_tanks_stats.py >> $LOGDIR/get_2020_tanks_stats.log 2>&1 # 4 mins
$PYTHON $SCRIPTSDIR/get_all_tanks_stats.py >> $LOGDIR/get_all_tanks_stats.log 2>&1 # 3 hours 14 mins

# populate the rest (last updated: all_tanks.csv / 2020_tanks.csv - above "data")
$PYTHON $SCRIPTSDIR/pop_awards_search.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_cups_leaderboard.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_stats_overall.py >> $STDLOG 2>&1
$PYTHON $SCRIPTSDIR/pop_stats_2020.py >> $STDLOG 2>&1

# push
git add .
git commit -a -m "Automated commit triggered."
git push origin master

# log
echo "Job ended: " $(date) >> $STDLOG
echo "Job ended: " $(date) >> $STDERR
echo "Job ended: " $(date) >> $STDOUT
