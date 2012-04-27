while [ 1 ]
do
echo "Collecting data for all stories run at $(date)"
python monitorUpcomingAndNewStories.py >> runLog001 2>>errLog001
python monitorDiggs.py >>runLog001 2>>errLog001
done

