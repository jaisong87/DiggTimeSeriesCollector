#This script updates all the author based features

import MySQLdb;
import sys

def getTitle(digg_id):
	db = MySQLdb.connect(user="root", passwd ="iltwat", db ="digg_newdatabase")
	conn = db.cursor()
	query = "SELECT title FROM diggs_upcoming_stories WHERE digg_id='%s'" % (digg_id)
	#print query
        conn.execute(query)
        ans = conn.fetchone()
        conn.close()
	if(ans != None):
	        return ans[0]
	else:
		return "ERROR"

def getDiggs(digg_id):
	db = MySQLdb.connect(user="root", passwd ="iltwat", db ="digg_newdatabase")
	conn = db.cursor()
	query = "SELECT diggs FROM diggs_upcoming_stories WHERE digg_id='%s'" % (digg_id)
	#print query
        conn.execute(query)
        ans = conn.fetchone()
        conn.close()
	if(ans != None):
	        return ans[0]
	else:
		return "ERROR"



def getStoryList():
	db = MySQLdb.connect(user="root", passwd ="iltwat", db ="digg_newdatabase")
        conn = db.cursor()
        query = "SELECT digg_id FROM diggs_final"
	#print query
        conn.execute(query)
        ans = conn.fetchall()
	conn.close()
	return ans

#stories = getStoryList()
#for story in stories:
#	updateAuthorFeatures(story[0])
