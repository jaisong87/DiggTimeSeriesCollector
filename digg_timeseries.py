'''
Created on Mar 17, 2012

@author: Pranesh-Sridharan (AceMcCloud)
'''
#
# @version: 1.0
#
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

diggwriter = csv.writer(open("Errortimeseries.csv", "wb"), delimiter='\t', quoting=csv.QUOTE_MINIMAL)

#
# Method to concatenate URL String
# @param Category:
# @param limit:  
# @param offset:
# 

def url_Concatenate(limit , offset , sort):

    # URL Domain of Digg Services API to fetch the  articles
    url_domain = 'http://services.digg.com/1.0/endpoint?method=story.getUpcoming&'
    diggargs ={ 'count': limit, 'offset': offset , 'sort':sort } #, 'min_date' : min_date }
    url_argument=urllib.urlencode(diggargs)
    return "%s%s" % (url_domain , url_argument)
    
    
#
# Method to fetch all Digg Articles from digg.com for a particular category
# @param offset:
# 

def get_News_Articles(offset):
  
    for off in range(1 ,offset):
        # Sorting order to fetch the articles which are posted recently
        sort = 'submit_date-desc'
        url = url_Concatenate(1 , off , sort)
        print url
        request = url
        
        try:
            response = urllib2.urlopen(request)
            response.read()
            xmlContent = urllib2.urlopen(request).read()
            
            # Getting the JSON contents in the data variable for processing
            node = parseString(xmlContent)

        except Exception as error:
                print "ERROR ", error 
                pass
        
        
        stories_count = node.getElementsByTagName('stories')[0].attributes['count'].value
        fetchTime = node.getElementsByTagName('stories')[0].attributes['timestamp'].value
        
        if stories_count == 0 :
            break
        else :
            #' Parsing the XML Nodes from the response '
            for data in node.getElementsByTagName('story'):
    
                # Getting the values needed to store in the database
                
               try:
                    digg_id = data.attributes['id'].value
                    digg_id.encode('utf8')
                    
                    url = data.attributes['href'].value
                    diggurl = data.attributes['link'].value
                    
                    comments = data.attributes['comments'].value
                    status = data.attributes['status'].value
                    
                    date = float(data.attributes['submit_date'].value)
                    diggs = data.attributes['diggs'].value
                    
               except Exception as error:
                   print "ERROR ", error 
                   pass
               
               try:
               
                    title = node.getElementsByTagName('title')[0].childNodes[0].nodeValue
                    title.encode('utf8')
               
               except Exception as error:
                       print "ERROR in title" , error
                       title = "undefined"
                       pass
               
               try:
               
                    description = node.getElementsByTagName('description')[0].childNodes[0].nodeValue
                    description.encode('utf8')
               
               except Exception as error:
                       print "ERROR in description" , error
                       description = "undefined"
                       pass
                 
               try:
                
                    userid = data.getElementsByTagName('user')[0].attributes['registered'].value
                
               except Exception as error:
                       print "ERROR in userid" , error
                       userid = "undefined"
                       pass
                   
               try: 
                   topic = data.getElementsByTagName('container')[0].attributes['short_name'].value
               except Exception as error:
                       print "ERROR in topic" , error
                       userid = "undefined"
                       pass
                
                    # Storing the information in the database 
                
            try:
                #print digg_id , url , diggurl
                #print "\n"
                #print datetime.fromtimestamp(date)
                
                # connection variable to connect to the Mysql Database
                conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "", db = "digg_newdatabase")
            except MySQLdb.Error, e:
                print "Error %d: %s\n" % (e.args[0], e.args[1])
                
            cursor = conn.cursor ()
            
                # Inserting the data to the Digg Database
            try:
                time.sleep(2);
                cursor.execute("INSERT INTO diggs_upcoming_stories(digg_id , url ,diggurl , categoryname , userid , postdate  , title , description ,diggs , noofcomments ,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(digg_id , url ,diggurl , topic , userid ,datetime.fromtimestamp(date)  , title , description , diggs ,comments ,status))
            except Exception as error:
                
                    # All Exceptions are Passed 
                    print digg_id
                    print "ERROR ", digg_id, error
                    diggwriter.writerow(digg_id)
                    time.sleep(1)
                    pass
            
            try:
                time.sleep(1);
                cursor.execute("INSERT INTO diggs_diggs(digg_id , digg_created , diggs , comments ) VALUES (%s,%s,%s,%s)",(digg_id ,datetime.fromtimestamp(date) , diggs ,comments))
            except Exception as error:
                
                    # All Exceptions are Passed 
                    print "ERROR ", digg_id, error
                    time.sleep(1)
                    pass
            
            cursor.close ()
            conn.commit()
            conn.close ()
            #diggwriter.close()
            
   
            
            


# Main Driver Code which inputs the topics/Category to fetch the news links.

get_News_Articles(500)
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             
                             