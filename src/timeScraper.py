import argparse
import operator
import sys
import urllib2
import sqlite3

import articleScraping

if __name__ == "__main__":

   conn = sqlite3.connect("redditTime.db")
   cursor = conn.cursor()
  
   cursor.execute("""CREATE TABLE if not exists newArticles
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer, timeScraped timestamp) 
               """)
   cursor.execute("""CREATE TABLE if not exists hotArticles
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer,timeScraped timestamp) 
               """)
               
               
   cursor.execute("""CREATE TABLE if not exists hotArticlesPositions
                  (id text, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer,timeScraped timestamp, position integer) 
               """)

  
   # Hot scraping
   articleScraping.scrapeHotArticlesPositionDependent('music', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('politics', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('worldnews', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('technology', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('pics', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('funny', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('aww', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('AskReddit', 50, cursor, conn, 'hotArticlesPositions')
   
   
   articleScraping.scrapeHotArticlesPositionDependent('chicago', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('programming', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('mildlyinteresting', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('explainlikeimfive', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('askscience', 50, cursor, conn, 'hotArticlesPositions')  
   articleScraping.scrapeHotArticlesPositionDependent('fffffffuuuuuuuuuuuu', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('gifs', 50, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('lifeprotips', 50, cursor, conn, 'hotArticlesPositions')