SCRIPTSDIR=/Users/thomas/git/tankpit-analytics.github.io/scripts
DATADIR=/Users/thomas/Desktop/tpdata
LOGDIR=/Users/thomas/Desktop/tpdata/log
PYTHON=/anaconda3/bin/python
STDLOG=$LOGDIR/update_5m.log
STDERR=$LOGDIR/update_5m.err
STDOUT=$LOGDIR/update_5m.out

# log
echo "#\nJob started: " $(date) >> $STDLOG
echo "#\nJob started: " $(date) >> $STDERR
echo "#\nJob started: " $(date) >> $STDOUT

# data - for each 5min data job, make sure to add start_5m_job_running() / stop_5m_job_running() methods
$PYTHON $SCRIPTSDIR/get_active.py >> $LOGDIR/get_active.log 2>&1
$PYTHON $SCRIPTSDIR/get_upcoming_tourn.py >> $LOGDIR/get_upcoming_tourn.log 2>&1
$PYTHON $SCRIPTSDIR/t100_overall_update.py >> $LOGDIR/t100_overall_update.log 2>&1 # 30 seconds
$PYTHON $SCRIPTSDIR/t100_2021_update.py >> $LOGDIR/t100_2021_update.log 2>&1 # 10 seconds

# log
echo "Job ended: " $(date) >> $STDLOG
echo "Job ended: " $(date) >> $STDERR
echo "Job ended: " $(date) >> $STDOUT
