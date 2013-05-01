#!/usr/bin/env python

"""

Created by Andreas Damgaard Pedersen 22 April 2012
Reddit username: _Daimon_
"""

import argparse
import operator
import sys
import urllib2
import sqlite3
import os


import articleScraping as a

 

if __name__ == "__main__":

   #dbPath="/Users/greg/localResearch/redditTest.db"
   dbPath = os.environ["REDDIT_EVOLUTION"]
   dbPath += "/redditEvolution.db" 
   conn = sqlite3.connect(dbPath)
   cursor = conn.cursor()
 
# create a table
   cursor.execute("""CREATE TABLE if not exists hotArticles
                  (id text, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer, timeScraped timestamp, position integer) 
               """)
   cursor.execute("""CREATE TABLE if not exists newArticles
                  (id text, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer, timeScraped timestamp, position integer) 
               """)

   reddits = ['politics', 'worldnews', 'uspolitics', 'liberal', 'progressive', 'conservative', 'technology', 'science', 
               'news', 'worldpolitics']

   for subreddit in reddits:
      a.scrapeNewArticlesPositionDependent(subreddit, 1000, cursor,conn,'newArticles')
      a.scrapeHotArticlesPositionDependent(subreddit, 1000, cursor,conn, 'hotArticles')   


   
 
   
   
   
   
   