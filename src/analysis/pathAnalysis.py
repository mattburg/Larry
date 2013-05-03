import sqlite3
import matplotlib
from pylab import *
from pandas import *
import numpy as np

####FIXXXX####
#need to look into how to create paths from new listing to hot listing, this is currently not well defined!!!

#dbPath = "/home/stoddardg/redditTime.db"
dbPath = "/Users/matthewburgess/Desktop/redditTime.db"
cursor = sqlite3.connect(dbPath).cursor()
        


#limit is mostly for debugging, if none is set then function loads entire table
def loadRawData(tableName,subredditName,limit=None):
    if limit == None:
         results = cursor.execute('SELECT * FROM %s WHERE subreddit="%s"' % (tableName,subredditName)).fetchall()
    else:
         results = cursor.execute('SELECT * FROM %s  WHERE subreddit="%s" limit %i' % (tableName,subredditName,limit)).fetchall()

    schema =  [x[1] for x in cursor.execute("PRAGMA table_info(%s);" % tableName).fetchall()]
    try:
        return DataFrame(results,columns = schema)
    except AssertionError:
        print "\nERROR: SQL query return null result, check query syntax\n" 
        exit()
    #print results

    '''df = DataFrame({'domains':results})
    grouped = df.groupby('domains')
    domainCounts = grouped.count()
    domainCounts = domainCounts.sort(columns=['domains'],ascending=False)
    domainCount = domainCounts.astype(float)/domainCounts.sum()
    print domainCount[0:k]
    print domainCount[0:k].sum()'''


#returns the paths for every post
def getPostPaths(df):
    postIds = df.id.unique() 
    postPaths = {}
    for postId in postIds:
       #sorts data by time scraped
       df = df.sort(['timeScraped'],ascending=True)
       #filters rows by post id
       post = df[df.id == postId]
       #selects position column
       post = post.position
       #bin paths by page so that each 25th position is grouped together
       path = [x/25 for x in post.values]
       postPaths[postId] = path
    return postPaths




if __name__ == "__main__":

   #dbPath = "/Users/greg/localResearch/redditDB.db"
   df = loadRawData("hotArticlesPositions","politics")
   print getPostPaths(df)
   
