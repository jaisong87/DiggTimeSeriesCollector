while [ 1 ]
do
echo "Collecting data for all stories run at $(date)" >> diggLog002
echo "Collecting data for all stories run at $(date)"
python monitorUpcomingAndNewStories.py >> runLog001
python monitorDiggs.py >> runLog001
done

