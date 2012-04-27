# This is a small script to monitor upcoming and top stories 
# across all digg categories continuosuly and update the database

from xml.dom.minidom import parseString
import urllib
import urllib2
import datetime
import time
import json
import MySQLdb
import csv
from pprint import pprint
from datetime import datetime

def getTopNewsUrl(limit, topic):
	baseUrl = 'http://services.digg.com/2.0/story.getTopNews?'
	params = { 'limit':limit, 'topic':topic }
	urlParams = urllib.urlencode(params)
	return "%s%s" % (baseUrl, urlParams)

def getUpcomingNewsUrl(limit, topic):
	baseUrl = 'http://services.digg.com/2.0/story.getUpcomingNews?'
	params = { 'limit':limit }
        urlParams = urllib.urlencode(params)
        return "%s%s" % (baseUrl, urlParams)

def getSocialDynamics(digg_id, date_created):
	result = { 'digg_id' :digg_id, 'date_created':date_created, 'tpc1':0,'tpc2':0,'tpc3':0,'tpc4':0,'tpc5':0, 'upc1':0,'upc2':0,'upc3':0,'upc4':0,'upc5':0 , 'uc':0}			
	res = (digg_id, date_created, 0,0,0,0,0,0,0,0,0,0,1)			
	try:
		db = MySQLdb.connect(user="root", passwd= "digg2012", db="Diggv2")
		conn = db.cursor()	
		query = "SELECT * FROM socialdynamics WHERE digg_id = '%s'" % (digg_id)
		conn.execute(query)
		res = conn.fetchone()
		if(res):
			result['tpc1']=res[2]
			result['tpc2']=res[3]
			result['tpc3']=res[4]
			result['tpc4']=res[5]
			result['tpc5']=res[6]
			result['upc1']=res[7]
			result['upc2']=res[8]
			result['upc3']=res[9]
			result['upc4']=res[10]
			result['upc5']=res[11]
			if res[12] :
				result['uc']=res[12]+1
			return result
		else:
			if int(date_created > (int(time.time())-60*310)):
				query1 = "INSERT INTO socialdynamics(digg_id, digg_created) VALUES('%s', '%s')" % (digg_id, datetime.fromtimestamp(date_created))
				#print query
				conn.execute(query1)
				query2 = "INSERT INTO diggs(digg_id, digg_created) VALUES('%s', '%s')" % (digg_id, datetime.fromtimestamp(date_created))
				conn.execute(query2)
		conn.close()
	except Exception as error:
		sys.stderr.write( str("%s : databse query(%s);(%s) failed %s" % (str(datetime.now()),query1,query2,error)) )
	return result

def updateSocialDynamics(story):
	try:
		db = MySQLdb.connect(user="root", passwd= "digg2012", db="Diggv2")
                conn = db.cursor()      
                query = "UPDATE socialdynamics SET tpc1=%d,tpc2=%d,tpc3=%d,tpc4=%d,tpc5=%d,upc1=%d,upc2=%d,upc3=%d,upc4=%d,upc5=%d,uc=%d WHERE digg_id = '%s'" % (story['tpc1'], story['tpc2'], story['tpc3'], story['tpc4'], story['tpc5'], story['upc1'], story['upc2'], story['upc3'], story['upc4'], story['upc5'], story['uc'],story['digg_id'])
		#print query
		conn.execute(query)
		conn.close()
	except Exception as error:
		sys.stderr.write(str("%s : databse query(%s) failed - %s" % (str(datetime.now()),query, error)))

	
def updateSectionFromTopList(topic, limit):
	request = getTopNewsUrl(limit, topic )
	storyCount = 0

	try:
		response = urllib2.urlopen(request)
        	result = response.read()
		jResult = json.loads(result)
		storyCount = jResult['count']	
	except Exception as error:
		sys.stderr.write(" %s : urlFetch Failed - %s: " % (str(datetime.now()),error))
	
	if storyCount > 0:
		for curStory in jResult['stories']:
			story_id = curStory['story_id']
			title = curStory['title']	
			date_created = curStory['date_created']
			story = getSocialDynamics(story_id, date_created)		
			t1 = datetime.fromtimestamp(time.time())
			t0 = datetime.fromtimestamp(date_created)
			dlt = t1-t0
			if dlt.days < 2 :
				if dlt.seconds < 3600 :
					story['tpc1'] = story['tpc1']+1	
				if dlt.seconds < 2*3600 :
					story['tpc2'] = story['tpc2']+1
				if dlt.seconds < 3*3600 :
					story['tpc3'] = story['tpc3']+1
				if dlt.seconds < 4*3600 :
					story['tpc4'] = story['tpc4']+1
				if dlt.seconds < 5*3600 :
					story['tpc5'] = story['tpc5']+1
				updateSocialDynamics(story)			
				#time.sleep(3)	


def updateSectionFromUpcomingList(topic, limit):
	request = getUpcomingNewsUrl(limit, topic )
	storyCount = 0

	try:
		response = urllib2.urlopen(request)
        	result = response.read()
		jResult = json.loads(result)
		storyCount = jResult['count']	
	except Exception as error:
		sys.stderr.write(" %s : urlFetch Failed! - %s " % (str(datetime.now()), error))

	if(storyCount>0) :
		for curStory in jResult['stories']:
			story_id = curStory['story_id']
			title = curStory['title']	
			date_created = curStory['date_created']
			story = getSocialDynamics(story_id, date_created)		
			t1 = datetime.fromtimestamp(time.time())
			t0 = datetime.fromtimestamp(date_created)
			dlt = t1-t0
			if dlt.days < 2 :
				if dlt.seconds < 3600 :
					story['upc1'] = story['upc1']+1	
				if dlt.seconds < 2*3600 :
					story['upc2'] = story['upc2']+1
				if dlt.seconds < 3*3600 :
					story['upc3'] = story['upc3']+1
				if dlt.seconds < 4*3600 :
					story['upc4'] = story['upc4']+1
				if dlt.seconds < 5*3600 :
					story['upc5'] = story['upc5']+1
				updateSocialDynamics(story)			
				#time.sleep(3)	

diggSections = [ "business", "entertainment", "gaming", "lifestyle", "offbeat", "politics", "science", "sports", "technology", "world_news" ]
print "%s : Updating the Tables from upcoming and top stories" % (str(datetime.now()))
updateSectionFromUpcomingList( "", 300)
for topic in diggSections:
	updateSectionFromTopList(topic,50)
