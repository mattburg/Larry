import argparse
import operator
import sys
import urllib2
import sqlite3

import articleScraping

if __name__ == "__main__":

   conn = sqlite3.connect("/Users/greg/localResearch/redditMusic.db")
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
   articleScraping.scrapeHotArticles('music', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeHotArticles('listentothis', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeHotArticlesPositionDependent('music', 25, cursor, conn, 'hotArticlesPositions')
   articleScraping.scrapeHotArticlesPositionDependent('listentothis', 25, cursor, conn, 'hotArticlesPositions')
   
   # New scraping
   articleScraping.scrapeNewArticles('music', 100, cursor, conn, 'newArticles')
   articleScraping.scrapeNewArticles('listentothis', 100, cursor, conn, 'newArticles')
   