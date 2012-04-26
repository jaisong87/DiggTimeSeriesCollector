from datetime import datetime
import urllib
import urllib2
import time
import MySQLdb
import json

def timeBefore(minutes):
	return "%s" % datetime.fromtimestamp(int(time.time())-minutes*60)
	
def getCurrentDiggCount(digg_id):
	request = "http://services.digg.com/2.0/story.getInfo?story_ids=%s" % digg_id
	try:
		response = urllib2.urlopen(request)
                result = response.read()
                jResult = json.loads(result)
                diggs = jResult['stories'][0]['diggs']
		return diggs
	except Exception as error:
		print "%s : %s Fetch failed!!!" % (str(datetime.now()),request), error 		
		return -1		

def getRecentDiggs(hour):
        try:
                db = MySQLdb.connect(user="root", passwd= "digg2012", db="Diggv2")
                conn = db.cursor()
                query = "SELECT * FROM diggs WHERE digg_created>'%s' AND digg_created<'%s'" % (timeBefore(hour*60+6), timeBefore(hour*60-6) )
	 	#print query
		conn.execute(query)
                res = conn.fetchall()
		conn.close()
		return res
	except Exception as error:
		print "%s : databse query(%s) failed" % (str(datetime.now()),query), error	

def updateDiggsTable(story):
	try:
		db = MySQLdb.connect(user="root", passwd= "digg2012", db="Diggv2")
		conn = db.cursor()
		query = "UPDATE diggs SET digg1=%d, digg2=%d, digg3=%d, digg4=%d, digg5=%d WHERE digg_id ='%s'" % (story['digg1'], story['digg2'], story['digg3'], story['digg4'], story['digg5'], story['digg_id'])
		#print query
		conn.execute(query)
		conn.close()
	except Exception as error:
                print "%s : databse query(%s) failed" % (str(datetime.now()),query), error


print "%s : Updating the Tables with diggCounts" % (str(datetime.now()))
for i in range(1,6):
	res = getRecentDiggs(i)
	if res :
		for row in res:
			story = {'digg_id':row[0], 'digg_created':row[1], 'digg1':row[2], 'digg2':row[3], 'digg3':row[4], 'digg4':row[5], 'digg5':row[6] }
			diggs = getCurrentDiggCount(story['digg_id'])
			if diggs <> -1 :
				index = "digg%s" % i
				story[index] = diggs
				updateDiggsTable(story) 				
