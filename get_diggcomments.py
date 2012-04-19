

'''
Created on Mar 17, 2012

@author: Pranesh-Sridharan (AceMcCloud)
'''
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
    conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "", db = "digg_database" , connect_timeout =300)
    
except MySQLdb.Error, e:
    print "Error %d: %s\n" % (e.args[0], e.args[1])
    
    
cursor = conn.cursor ()
category = 'technology'
    # Getting the Category ID for the corresponding topic from the database
cursor.execute("SELECT digg_id , noofcomments FROM diggs_search_stories_mindate WHERE categoryname = %s" , category)
                
row = cursor.fetchall ()
total_rows = cursor.rowcount
print total_rows
    
for i in range(100, total_rows):
        
    story_id = row[i][0]
    limit = row[i][1]
    print story_id , limit
            # URL Domain of Digg Services API to fetch the  articles
    url_domain = 'http://services.digg.com/2.0/story.getComments?'
    diggargs ={ 'story_id': story_id , 'limit': limit }
    url_argument=urllib.urlencode(diggargs)
    request =  "%s%s" % (url_domain , url_argument)
    print request
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
            print data['count']
            time.sleep(3)
                
            diggs = data['comments'][index]['diggs']
            user_id = data['comments'][index]['user']['user_id']
            comment_id = diggsup = data['comments'][index]['comment_id']
            thread_id = diggsup = data['comments'][index]['thread_id']
            comment_text = data['comments'][index]['text']
            comment_parentid = data['comments'][index]['parent_id']
            story_id = data['comments'][index]['story_id']
            date_created = data['comments'][index]['date_created']
            diggs_up = data['comments'][index]['up']
            diggs_down = data['comments'][index]['down']
            
            if(comment_parentid is None):
                comment_parentid = 'PARENT' 
                
                print conn
                # Inserting the data to the Digg Database
                cursor2 = conn.cursor()
                print cursor2
            try :    
                cursor2.execute("INSERT INTO digg_comments(id , story_id , thread_id , userid , postdate , comment_text , diggs , diggsup , diggsdown , parent_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (comment_id , story_id , thread_id , user_id , datetime.fromtimestamp(date_created) , comment_text , diggs , diggs_up , diggs_down , comment_parentid))
                print cursor2.rowcount
                conn.commit()
                time.sleep(1)
            except Exception as error:
                
                    # All Exceptions are Passed 
                    print "ERROR ", index , comment_id, error
                    time.sleep(1)
                    pass

cursor2.close ()
cursor.close()
conn.commit()
conn.close()