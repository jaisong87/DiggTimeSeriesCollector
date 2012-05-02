#This script updates all the author based features

import MySQLdb;
import sys

def getAuthor(digg_id):
	db = MySQLdb.connect(user="root", passwd ="", db ="digg_newdatabase")
	conn = db.cursor()
	query = "SELECT userid FROM diggs_upcoming_stories WHERE digg_id='%s'" % (digg_id)
	#print query
        conn.execute(query)
        ans = conn.fetchone()
        conn.close()
	if(ans != None):
	        return ans[0]
	else:
		return -7777

def getAuthorInfo(authorid, param):
        db = MySQLdb.connect(user="root", passwd ="", db ="digg_newdatabase")
        conn = db.cursor()
        query = "SELECT %s FROM digg_users WHERE userid=%d" % (param,int(authorid))
        #print query
        conn.execute(query)
        ans = conn.fetchone()
        conn.close()
	if(ans != None):
	        return ans[0]
	else:
		return -7777

def getStoryList():
	db = MySQLdb.connect(user="root", passwd ="", db ="digg_newdatabase")
        conn = db.cursor()
        query = "SELECT digg_id FROM diggs_final"
	#print query
        conn.execute(query)
        ans = conn.fetchall()
	conn.close()
	return ans

def updateAuthorFeatures(digg_id):
	author = getAuthor(digg_id)
	if(author != 'undefined'):
		authorDiggs = getAuthorInfo(author, 'diggs')     
		authorComments = getAuthorInfo(author, 'comments')
		authorFans = getAuthorInfo(author, 'followers')
		authorFollows = getAuthorInfo(author, 'following') 
		authorGender = getAuthorInfo(author, 'gender' )
		authorSubmissions = getAuthorInfo(author, 'submissions')
		db = MySQLdb.connect(user="root", passwd ="", db ="digg_newdatabase")
	        conn = db.cursor()
		query = "UPDATE diggs_final SET authorDiggs = %d, authorComments = %d, authorFans = %d , authorFollows = %d , authorGender = '%s', authorSubmissions = %d WHERE digg_id = '%s'" % (authorDiggs, authorComments, authorFans, authorFollows, authorGender, authorSubmissions, digg_id)
		print query , " [ Author is : ", author, " ]\n"
		conn.execute(query)
		conn.close()
	else:
		sys.stderr.write("Error! - Author is undefined\n")


stories = getStoryList()
for story in stories:
	updateAuthorFeatures(story[0])
