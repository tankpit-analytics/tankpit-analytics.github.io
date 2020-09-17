# this will run hourly besides at night when daily is running (setting this up only on cron...)
# */15 06-23 * * *

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

# push
git add .
git commit -a -m "Automated hourly commit triggered."
git push origin master

# log
echo "Job ended: " $(date) >> $STDLOG
echo "Job ended: " $(date) >> $STDERR
echo "Job ended: " $(date) >> $STDOUT
