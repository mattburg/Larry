##this is a script that downloads all the webpages for creating the
##political sentiment classifier

import urllib2
import os
import sys
from pprint import pprint
from database import Database
from collections import defaultdict


db = Database()
categories = ['Liberal','Conservative','progressive','democrats','republicans']

for category in categories:
    
    urlCount = defaultdict(lambda :0)
    results = db.cursor.execute('SELECT domain FROM trainingData WHERE subreddit = ?',(category,))

    for url in results:
        urlCount[url]+=1

        '''try:
            html = urllib2.urlopen(url[0]).read()
            print html
        except urllib2.HTTPError:
            continue'''


    print category,"\n\n\n"
    pprint (sorted(urlCount.items(),key = lambda x:x[1],reverse=True))
    

