

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
    conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "", db = "DiggTimeSeriesCollector" , connect_timeout =300)
    
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
            time.sleep(1)
                
            diggs = data['stories'][index]['diggs']
            story_id = data['stories'][index]['story_id']
            date_created = data['stories'][index]['date_created']
            comments = data['stories'][index]['comments']
                
            print conn
                # Inserting the data to the Digg Database
            cursor2 = conn.cursor()
            print cursor2
        try :    
            cursor2.execute("INSERT INTO diggs_diggs(digg_id , digg_created , diggs , comments ) VALUES (%s,%s,%s,%s)",(story_id ,datetime.fromtimestamp(date_created) , diggs ,comments))
            print cursor2.rowcount
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
