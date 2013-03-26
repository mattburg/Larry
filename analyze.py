import sqlite3
import matplotlib
from pylab import *
from pandas import *
import numpy as np

def dict_from_row(row):
    return dict(zip(row.keys(), row))

def plotScoresByDomain():
   query = "SELECT T.domain, T.title, T.dateCreated, T.score FROM topArticles T \
            WHERE T.subreddit=\"politics\"  \
            ORDER BY T.domain"
   cursor.execute(query)
   results = cursor.fetchall()
   allResults = []
   domains = set()
   for result in results:
      print result['domain']
      domains.add(result['domain'])
      print result.keys()
      allResults.append(dict_from_row(result))
   
   df = DataFrame(allResults)
   #print df
   #print df[ df["score"] > 500]
   
   for domain in domains:
      if(df[ df['domain'] == domain]["score"].count() < 100):
         continue
      print domain
      print df[ df['domain'] == domain]["score"].mean()
      print df[ df['domain'] == domain]["score"].std()
      
      
   grouped = df.groupby("domain")
   print grouped
   print len(grouped)
   print grouped.size()
   
   print grouped['score'].mean() 
   #print grouped['score'].std()
   print grouped['score'].median()


def examineByTime():
      timeQuery = "SELECT T.domain, T.title, T.dateCreated, T.score FROM topArticles T \
               WHERE T.subreddit=\"politics\" \
               ORDER BY T.dateCreated"
      
      cursor.execute(timeQuery)
      results = cursor.fetchall()
      timeValues = []
      scoreValues = []
      for result in results:
         if(result['score'] < 500):
            continue
         timeValues.append(result['dateCreated'])
         scoreValues.append(result['score'])
      scatter(timeValues, scoreValues)

def examineSuccessRates():
   worldNewsSuccessQuery = "SELECT Top.Domain, New.NewCount, Top.TopCount, Top.TopAverage \
   FROM (SELECT T.domain AS domain, COUNT(T.domain) as TopCOUNT, AVG(T.score) as TopAverage FROM topArticles T where T.subreddit=\"worldnews\" GROUP BY T.domain) AS Top,\
   (SELECT S.domain AS domain, COUNT(S.domain) as NewCOUNT FROM newArticles S where S.subreddit=\"worldnews\" GROUP BY S.domain) AS New \
   WHERE New.domain=Top.domain"
   
   usPoliticsSuccessQuery = "SELECT Top.Domain, New.NewCount, Top.TopCount, Top.TopAverage \
   FROM (SELECT T.domain AS domain, COUNT(T.domain) as TopCOUNT, AVG(T.score) as TopAverage FROM topArticles T where T.subreddit=\"uspolitics\" GROUP BY T.domain) AS Top,\
   (SELECT S.domain AS domain, COUNT(S.domain) as NewCOUNT FROM newArticles S where S.subreddit=\"uspolitics\" GROUP BY S.domain) AS New \
   WHERE New.domain=Top.domain"
  
   politicsSuccessQuery = "SELECT Top.Domain, New.NewCount, Top.TopCount, Top.TopAverage \
   FROM (SELECT T.domain AS domain, COUNT(T.domain) as TopCOUNT, AVG(T.score) as TopAverage FROM topArticles T where T.subreddit=\"politics\" GROUP BY T.domain) AS Top,\
   (SELECT S.domain AS domain, COUNT(S.domain) as NewCOUNT FROM newArticles S where S.subreddit=\"politics\" GROUP BY S.domain) AS New \
   WHERE New.domain=Top.domain \
   ORDER BY Top.TopAverage"
   

                  
   cursor.execute(politicsSuccessQuery)
   #cursor.execute(worldNewsSuccessQuery)
   #cursor.execute(usPoliticsSuccessQuery)
   #results = cursor.fetchmany(size=10)
   results = cursor.fetchall()
   #print results
   xValues = []
   yValues = []
   successValues = []
   averageScoreValues = []
   domainNames = []
   for result in results: 
      #print result.keys()
      #if( result['NewCOUNT'] < 10):
      #   continue
      if( result['TopCOUNT'] < 15):
         continue
      percentSuccess = result['TopCount']/(1.0*result['NewCount'])
      print result['domain'] + " " + str(percentSuccess) + " " + str(result['TopAverage'])
      print result['domain'] + " " + str(result['NewCount'])
      xValues.append(result['NewCount'])
      yValues.append(result['TopCount'])
      successValues.append(percentSuccess)
      domainNames.append(result['domain'] + " " + str(percentSuccess))
      averageScoreValues.append(result['TopAverage'])
   print(sum(yValues))
   #hist(xValues, bins=25)   
   scatter(successValues, averageScoreValues)  
   #hist(successValues, bins=50, label="test")  
   #pie(successValues, labels=domainNames, startangle=90)
   #scatter(xValues, yValues)

if __name__ == "__main__":

   dbPath = "/Users/greg/localResearch/redditDB.db"
   conn = sqlite3.connect(dbPath)
   
   conn.row_factory = sqlite3.Row
   
   cursor = conn.cursor()
   
   #examineByTime()
   #examineSuccessRates()
   plotScoresByDomain()
   show()