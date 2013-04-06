import argparse
import operator
import sys
import urllib2
import sqlite3

import articleScraping

if __name__ == "__main__":

   conn = sqlite3.connect("mydatabase.db")
   cursor = conn.cursor()
  
   cursor.execute("""CREATE TABLE if not exists trainingData
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer) 
               """)

  
   # Liberal subreddits
   articleScraping.scrapeHotArticles('liberal', 1000, cursor, conn, 'trainingData')
   articleScraping.scrapeHotArticles('Progressive', 1000, cursor, conn, 'trainingData')
   articleScraping.scrapeHotArticles('Democrats', 1000, cursor, conn, 'trainingData')
   
   #Conservative subreddits
   articleScraping.scrapeHotArticles('conservative', 1000, cursor, conn, 'trainingData')
   articleScraping.scrapeHotArticles('republicans', 1000, cursor, conn, 'trainingData')
   #articleScraping.scrapeHotArticles('liberal', 1000, cursor, conn, 'trainingData')
   