import matplotlib 
matplotlib.use('Agg')

import matplotlib.pyplot as plt



import sqlite3
import networkx as nx

from pandas import *
import numpy as np
from datetime import date



from pylab import *

from dateutil import parser

from datetime import datetime, timedelta

####FIXXXX####
#need to look into how to create paths from new listing to hot listing, this is currently not well defined!!!



#We should really put an index on IDs for both tables, to allow for faster grabbing of results

dbPath = "/z/reddit/redditEvolutionBackup.db"
#dbPath = "/Users/matthewburgess/Desktop/redditTime.db"
cursor = sqlite3.connect(dbPath).cursor()


def createIndex():
   hotIndex = "CREATE INDEX idIndex ON hotArticles (id)"
   newIndex =  "CREATE INDEX idIndex2 ON newArticles (id)"
   #cursor.execute(hotIndex)
   cursor.execute(newIndex)

def loadRawDataLimitArticles(tableName,subredditName, limit):
   
   idQuery= 'SELECT DISTINCT ID FROM ' + tableName + ' WHERE subreddit=(?) ORDER BY RANDOM() LIMIT (?)'
   articleIDs = cursor.execute(idQuery,[subredditName, limit]).fetchall()
   hotQuery = 'SELECT * FROM hotArticles WHERE id=(?)'
   newQuery = 'SELECT * FROM newArticles WHERE id=(?)'
   
   allHotResults = []
   allNewResults = []
   for row in articleIDs:
      id = row[0]
      #print id
      hotResults = cursor.execute(hotQuery, [id])
      allHotResults += list(hotResults)
      newResults = cursor.execute(newQuery, [id])
      allNewResults += list(newResults)
   
   schema =  [x[1] for x in cursor.execute("PRAGMA table_info(%s);" % tableName).fetchall()]
   print "# hot results = " + str(len(allHotResults))
   print "# new results = " + str(len(allNewResults))
   hotDF = DataFrame(allHotResults, columns = schema)
   hotDF['ranking'] = 'hot'
   newDF = DataFrame(allNewResults, columns = schema)
   newDF['ranking'] = 'new'
   
   return concat([newDF, hotDF])


        
        
        

#calculate lengths of time on front page
#need to attempt to control for time of day the article made it to the front page
def frontPageTimes(subreddit):
   
   
   
   query = '''SELECT t.url, MIN(t.timeScraped) as minTime, MAX(t.timeScraped) as maxTime FROM hotArticles t WHERE
               t.subreddit = (?) AND
               t.position <= 25
            GROUP BY t.url'''  
            
   cursor.execute(query, [subreddit])
   timeLengths = []
   timeByHour = [ [] for i in (0,1,2) ]
   results = cursor.fetchall()
   for result in results:
      maxTime = parser.parse(result[2])
      minTime = parser.parse(result[1])
      #print "minTime is " + str(minTime)
      #print minTime.hour
      diff = maxTime - minTime
      
      timeOfDay = minTime.hour/8
      
      timeByHour[timeOfDay].append(diff.total_seconds())
      
      timeLengths.append(diff.total_seconds())      
        
   bins = [ i*3600 for i in range(1,24)]
   print bins
   print len(timeLengths)    
   plt.hist(timeLengths, bins=bins)
   plt.title("All articles")
   
   plt.figure(2)
   plt.hist(timeByHour[0], bins=bins)
   plt.title("12am to 8am")
   
   plt.figure(3)
   plt.hist(timeByHour[1], bins=bins)
   plt.title("8am to 4pm")
   
   
   plt.figure(4)
   plt.hist(timeByHour[2], bins=bins)
   plt.title("4pm to 12am")
   
   
   plt.savefig(subreddit + '_times.png')
   
def plotRandomLinks(limit=10):
   query = '''SELECT * FROM 
            (SELECT S.url as url, S.subreddit as subreddit , COUNT(s.url) as numEntries, MIN(s.position) as minPos FROM hotArticlesPositions S
            GROUP BY S.url) T 
            WHERE numEntries >= 50 AND
            minPos < 25
            ORDER BY random()
            LIMIT (?)
            '''
        
   cursor.execute(query, [limit])
   results = cursor.fetchall()
   i = 0 
   for result in results:
      plt.figure(i)
      getThresholdGraph(result[0], result[1])
      i += 1
def getThresholdGraph(url, subreddit):
   df = loadRawData("hotArticlesPositions", subreddit)
   
   (scores, thresholds, lowerScores, times) =  calculateThresholds( url, df)
   #plt.plot(times, scores, times, thresholds, times, lowerScores)
   
   plt.plot(times, scores, times, thresholds)
   return (scores, thresholds, lowerScores, times)
   
def calcScore(x):
   createdTime = datetime.fromtimestamp(x['dateCreated'])
   scrapeTime = parser.parse(x['timeScraped'])
      #print scrapeTime
      #print result['timeScraped']
      
      
   timeDifference = createdTime - scrapeTime
   
   

   return np.log10(x['score']) + (1/45000.0)*timeDifference.total_seconds()
   
   
def calculateThresholds(articleURL, df):
   timeConstant = (1)/(45000.0)
   frontPageTimes = df[ df['url']==articleURL]
   frontPageTimes = frontPageTimes[frontPageTimes['position'] <= 25]
   
   indices = frontPageTimes.index
   
   thresholds = []
   scores = []
   lowerScores = []
   
   
   scorePairs = []
   pairs = [] 
   times = []
   
   for index in indices:
      #print 'index is ' + str(index)
      baseIndex = 50*(index/50)
      
      
      
      articleRow = df.ix[index]
      thresholdRow = df.ix[(baseIndex + 25)]
      
      articleTime = datetime.fromtimestamp(articleRow['dateCreated'])
      thresholdTime = datetime.fromtimestamp(thresholdRow['dateCreated'])
      scrapeTime = parser.parse(articleRow['timeScraped'])
      
      #timeDifference = articleTime - thresholdTime
      timeDifference = thresholdTime - articleTime
      #print timeDifference.total_seconds()
      #print timeConstant*timeDifference.total_seconds()
      
      exponent = timeConstant*timeDifference.total_seconds()
      
      thresholdScore = thresholdRow['score']*np.power(10, exponent)
      #print thresholdScore
      thresholds.append(thresholdScore)
      scores.append(articleRow['score'])
      lowerScores.append(thresholdRow['score'])
      
      pairs.append( (articleRow['score'], thresholdScore) )
      
      scorePairs.append( (calcScore(articleRow), calcScore(thresholdRow)) )
      
      times.append(scrapeTime)
      
   
   return (scores, thresholds, lowerScores,  times)
   
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


def getPostPathsWithTime(df):
    postIds = df.id.unique() 
    postPaths = {}
    for postId in postIds:
       #sorts data by time scraped
       df = df.sort(['timeScraped'],ascending=True)
       #filters rows by post id
       post = df[df.id == postId]

       test = post[ ['timeScraped','ranking','position']]
       test['position'] = ((test['position'] - 1)/25) + 1
       path = []
       for i in range(len(test)):
         currentRow =  test.irow(i)
         path.append( [currentRow['timeScraped'], currentRow['ranking'], currentRow['position']])
       postPaths[postId] = path
    return postPaths


#returns the paths for every post
def getPostPaths(df):
    postIds = df.id.unique() 
    postPaths = {}
    for postId in postIds:
       #sorts data by time scraped
       df = df.sort(['timeScraped'],ascending=True)
       #filters rows by post id
       post = df[df.id == postId]
       #print post
       #selects position column
       post = post.position
       #print post
       print post.values
       #bin paths by page so that each 25th position is grouped together
       path = [x/25 for x in post.values]
       postPaths[postId] = path
    return postPaths
    

#path is an array of triples <t,r,p> where t is timescraped, r is the rankinng (either hot or new), and p is the page number (from 1 to 40)
#should return a list of pairs indicating the start and end node for each edge
def processPath(path):

   edges = []
   lastTime = 0
   for node in path:
      #print node
      if node[1] == 'new':
         continue      
      currentNodeName = node[1] + str(node[2])
      if node[2] > 8:
         currentNodeName = "8+"
      currentTime = parser.parse(node[0])
      
      #hack to deal with when there is no last node
      if lastTime == 0:
         edge = ("ENTER", currentNodeName)
         edges.append(edge)
         prevNodeName = currentNodeName
         lastTime = currentTime
         continue
      
      timeDifference = currentTime - lastTime
     
      if timeDifference.total_seconds() < 900: # of seconds in 15 minutes
         edge = (prevNodeName, currentNodeName)
         edges.append(edge)
         
      prevNodeName = currentNodeName
      lastTime = currentTime
    
   return edges
   
   
def processAllPaths(paths):
   edgeWeights = {}
   for path in paths.values():
      
      normalizedPath = processPath(path)
      for edge in normalizedPath:
         try:
            edgeWeights[edge] += 1
         except:
            edgeWeights[edge] = 1
   
   G = nx.DiGraph()      
   for edge in edgeWeights.keys():
      G.add_weighted_edges_from( [(edge[0],edge[1], edgeWeights[edge]) ] )
       
   nx.write_dot(G, "test.dot")


def createEvolutionGraph(subreddit, numArticles=500):
   df = loadRawDataLimitArticles('hotArticles', subreddit, numArticles)
   paths = getPostPathsWithTime(df)
   processAllPaths(paths)   
   
def blah():
   beginDate = date(2013, 5, 4)
   endDate = date(2013, 5, 6)
   hotDF = loadRawDataDates("hotArticles", "politics", beginDate, endDate, limit=100000)
   hotDF["ranking"] = "hot"
   #print hotDF
   #current hack to deal with the fact that I dont have data for the new page yet
   newDF = loadRawDataDates("newArticles", "politics", beginDate, endDate, limit=100000)
   newDF["ranking"] = "new"
   #print newDF
   
   #contains all data from hot and new queue, along with labels
   wholeDF = concat([newDF, hotDF])
   return wholeDF
def main():
   df = loadRawData("hotArticles","politics", limit=100)
   
   paths = getPostPathsWithTime(df)
   for id in paths.keys():
      print "ID is " + str(id)
      print "Data is " 
      print paths[id]

if __name__ == "__main__":

   #dbPath = "/Users/greg/localResearch/redditDB.db"
   df = loadRawData("hotArticles","politics", limit=100)
   paths = getPostPaths(df)
   for id in paths.keys:
      print "ID is " + str(id)
      print "Data is " 
      print paths[id]
      
      
      
      
      
      
      
      
      
      
      
      
