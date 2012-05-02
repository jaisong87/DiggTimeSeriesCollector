'''
Created on Apr 27, 2012

@author: AceMccloud
'''

' This Script gets the User Information which includes the followers , Submissions'
'Total count of diggs received , comments commented by the user .'

#
# @version: 1.0
#
from xml.dom.minidom import parseString
import urllib
import datetime 
import time
import json
import MySQLdb
import csv
from pprint import pprint
from datetime import datetime

        

# Main Driver Code which inputs the topics/Category to fetch the news links.
try:    
    # connection variable to connect to the Mysql Database
    conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "iltwat", db = "digg_newdatabase" , connect_timeout =300)
    
except MySQLdb.Error, e:
    print "Error %d: %s\n" % (e.args[0], e.args[1])
    
    
cursor = conn.cursor ()
    # Getting the Category ID for the corresponding topic from the database
cursor.execute("SELECT digg_id FROM diggs_upcoming_stories")
                
row = cursor.fetchall ()
total_rows = cursor.rowcount
print total_rows
    
for i in range(1, total_rows):
        
    story_id = row[i][0]
    
    # URL Domain of Digg Services API to fetch the  articles
    url_domain = 'http://services.digg.com/2.0/story.getInfo?'
    diggargs ={ 'story_ids': story_id  }
    url_argument=urllib.urlencode(diggargs)
    request =  "%s%s" % (url_domain , url_argument)
    #print request
    try:
        response = urllib.urlopen(request)
        response.read()
        jsonContent = urllib.urlopen(request).read()
    
        # Getting the JSON contents in the data variable for processing
        data = json.loads(jsonContent)

    except Exception as error:
        print "ERROR ", error 
        pass
    
    if data['count'] != 0:
        #print jsonContent 
        for index in range(0 , data['count']):
            #print data['count']
            time.sleep(1)
                
            digg_id = data['stories'][index]['story_id']
            digg_id.encode('utf8')
            username = data['stories'][index]['submiter']['username']
            user_id = data['stories'][index]['submiter']['user_id']
            gender = data['stories'][index]['submiter']['gender']
            diggs = data['stories'][index]['submiter']['diggs']
            comments = data['stories'][index]['submiter']['comments']
            followers = data['stories'][index]['submiter']['followers']
            following = data['stories'][index]['submiter']['following']
            submissions = data['stories'][index]['submiter']['submissions']
            #print 'username' ,username
            #print 'user_id', user_id
            #print conn
                # Inserting the data to the Digg Database
            cursor2 = conn.cursor()
            #print cursor2
            
        #=======================================================================
        #    # URL Domain of Digg Services API to fetch the  articles
        #    url_domain = 'http://services.digg.com/2.0/user.getInfo?'
        #    diggargs ={ 'usernames': username  }
        #    url_argument=urllib.urlencode(diggargs)
        #    request =  "%s%s" % (url_domain , url_argument)
        #    print request
        #    try:
        #        response = urllib.urlopen(request)
        #        response.read()
        #        jsonContent = urllib.urlopen(request).read()
        #    
        #        # Getting the JSON contents in the data variable for processing
        #        userdata = json.loads(jsonContent)
        # 
        #    except Exception as error:
        #        print "ERROR ", error 
        #        pass
        #    
        #=======================================================================
        try :    
            cursor2.execute("INSERT INTO digg_users(userid, username, gender, followers , following , submissions , comments ,diggs , digg_id)VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_id, username , gender , followers , following , submissions, comments , diggs , story_id))
            #print cursor2.rowcount 
            conn.commit()
            time.sleep(1)
        except Exception as error:
            
                # All Exceptions are Passed 
                print "ERROR ", index , error
                time.sleep(1)
                pass

cursor2.close ()
cursor.close()
conn.commit()
conn.close()
