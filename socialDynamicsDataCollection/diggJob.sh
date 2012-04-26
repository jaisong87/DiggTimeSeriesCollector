while [ 1 ]
do
echo "Collecting data for all stories run at $(date)" >> diggLog002
python monitorUpcomingAndNewStories.py
python monitorDiggs.py
done

