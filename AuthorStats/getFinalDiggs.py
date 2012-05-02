import getDiggs
import MySQLdb
import json

f = open("diggUpdate1.sql", 'w')
f.write("USE DiggTimeSeriesApr12;\n")
try:
	db = MySQLdb.connect(user="root", passwd = "", db = "DiggTimeSeriesApr12")
	conn = db.cursor()
	conn.execute("SELECT digg_id FROM diggs_final WHERE diggs<0")# OR fofCount<0")
	stories = conn.fetchall()
	conn.close()
	print "Going to Fetch details of %d stories\n" % len(stories)
except Exception as error:
	print "Getting TODO-DiggList failed ! - %s\n" % error

for story in stories:
	dc = getDiggs.getCurrentDiggCount(story[0])
	try:
		db = MySQLdb.connect(user="root", passwd = "", db = "DiggTimeSeriesApr12")
		conn = db.cursor()
		query = "UPDATE diggs_final SET diggs=%d WHERE digg_id='%s'" % (int(dc), story[0])
		fquery = "UPDATE diggs_final SET diggs=%d WHERE digg_id='%s';\n" % (int(dc), story[0])
		conn.execute(query) 
		conn.close()
		f.write( fquery ) 
	except Exception as error:
		print "Insert into DB failed! - %s\n" % error
