from datetime import datetime
import urllib
import urllib2
import time
import MySQLdb
import json

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
