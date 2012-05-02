'''
Created on Apr 27, 2012

@author: AceMccloud
'''

' This Script gets the User Information of Fans of Fans'


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

        

digg_cursor = ''
# Main Driver Code which inputs the topics/Category to fetch the news links.
try:    
    # connection variable to connect to the Mysql Database
    conn = MySQLdb.connect (host = "localhost",user = "root",passwd = "", db = "digg_newdatabase" , connect_timeout =300)
    
except MySQLdb.Error, e:
    print "Error %d: %s\n" % (e.args[0], e.args[1])
    
    
cursor = conn.cursor ()
    # Getting the Category ID for the corresponding topic from the database
cursor.execute("SELECT userid , username , followers FROM digg_users")
                
row = cursor.fetchall ()
total_rows = cursor.rowcount
print total_rows
    
for i in range(0, total_rows):
        
    user_id = row[i][0]
    username = row[i][1]
    user_followers = row[i][2]
    limit = 1
    
    print user_followers
    for j in range(1 , user_followers):
    # URL Domain of Digg Services API to fetch the user followers
        url_domain = 'http://services.digg.com/2.0/user.getFollowers?'
        diggargs ={ 'username': username , 'cursor' : digg_cursor , 'limit'  : limit }
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
    
        digg_cursor = data['cursor']    
        if data['count'] != 0:
            #print jsonContent 
            for index in range(0 , data['count']):
                print data['count']
                time.sleep(1)
                    
                follower_username = data['followers'][index]['username']
                follower_userid = data['followers'][index]['user_id']
                gender = data['followers'][index]['gender']
                diggs = data['followers'][index]['diggs']
                comments = data['followers'][index]['comments']
                followers = data['followers'][index]['followers']
                following = data['followers'][index]['following']
                submissions = data['followers'][index]['submissions']
                print 'username' ,username
                print 'user_id', user_id
                print conn
                    # Inserting the data to the Digg Database
                cursor2 = conn.cursor()
                print cursor2
            
            try :    
                cursor2.execute("INSERT INTO diggs_followers(userid, username, following_userid , following_username , gender, followers , following , submissions , comments ,diggs , url) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(follower_userid ,follower_username ,user_id, username , gender , followers , following , submissions, comments , diggs , request))
                print cursor2.rowcount 
                conn.commit()
                time.sleep(2)
            except Exception as error:
                
                    # All Exceptions are Passed 
                    print "ERROR ", index , error
                    time.sleep(1)
                    pass

    cursor2.close ()
    cursor.close()
    conn.commit()
    conn.close()