from datetime import datetime
import urllib
import urllib2
import time
import MySQLdb
import json
import sys

def getCurrentDiggCount(digg_id):
        request = "http://services.digg.com/2.0/story.getInfo?story_ids=%s" % digg_id
        try:
                response = urllib2.urlopen(request)
                result = response.read()
                jResult = json.loads(result)
                diggs = jResult['stories'][0]['diggs']
                return diggs
        except Exception as error:
                sys.stderr.write( "%s : %s Fetch failed!!! - %s" % (str(datetime.now()),request, error))
                return -1


def updateDiggTable(digg_id, fh):
	try:
		db = MySQLdb.connect(user="root", passwd = "", db = "X1Diggv2")
		conn = db.cursor()
		queryP = "SELECT * FROM diggFeatures WHERE digg_id = '%s'" % (digg_id)
		conn.execute(queryP)
		ans = conn.fetchone()
		if(ans != None):
			digg = ans[0]
		else:
			digg = getCurrentDiggCount(digg_id)
		query = "INSERT IGNORE INTO diggFeatures(digg_id, diggs) VALUES('%s', %d)" % (digg_id, digg) 
		query1 = "%s;\n" % (query)
		print query1
		fh.write(query1)	
		conn.execute(query)
		#conn.commit()
		conn.close()
	except Exception as error:
		print "DB-operation Failed! ", error
		time.sleep(1)
		
def getStories():
	try:
		db = MySQLdb.connect(user="root", passwd = "", db = "X1Diggv2")
                conn = db.cursor()
                query = "SELECT digg_id FROM diggs WHERE digg_created < '2012-04-30 02:10:00' AND digg5>2"
                conn.execute(query)
		diggs = conn.fetchall()
		conn.close()
		return diggs
        except Exception as error:
                print "DB-operation Failed! ", error
		diggs = []
		return diggs

fh = open("diggFeatures.sql", "w")
fh.write("USE X1Diggv2;\n")
stories = getStories()
for story in stories:
	updateDiggTable(story[0], fh)
fh.close()
