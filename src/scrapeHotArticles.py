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


import praw
import articleScraping



      
def scrapeHotArticles(subreddit):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   hotSubmissions = r.get_subreddit(subreddit).get_hot(limit=25)
   #print "top submissions"
   for thing in hotSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments]
      
      cursor.execute('INSERT OR REPLACE INTO topArticles values (?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit()


 

if __name__ == "__main__":

   dbPath="/Users/greg/localResearch/redditPoliticalDB.db"
   
    #Dropbox/research/crowdCuration/code/redditScraper/mydatabase.db"

   conn = sqlite3.connect(dbPath)
   cursor = conn.cursor()
 
# create a table
   cursor.execute("""CREATE TABLE if not exists hotArticles
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer, timeScraped timestamp) 
               """)
   cursor.execute("""CREATE TABLE if not exists newArticles
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer, timeScraped timestamp) 
               """)

   #scrapeHotArticles('politics')
   #scrapeHotArticles('worldnews')
   #scrapeHotArticles('uspolitics')
   
   #scrapeHotArticles('liberal')
   #scrapeHotArticles('democrats')
   #scrapeHotArticles('progressive')
   
   #scrapeHotArticles('conservative')
   #scrapeHotArticles('republicans')
   
   articleScraping.scrapeNewArticles('politics', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeNewArticles('worldnews', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeNewArticles('uspolitics', 25, cursor, conn, 'hotArticles')
   
   articleScraping.scrapeNewArticles('liberal', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeNewArticles('democrats', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeNewArticles('progressive', 25, cursor, conn, 'hotArticles')
   
   articleScraping.scrapeNewArticles('conservative', 25, cursor, conn, 'hotArticles')
   articleScraping.scrapeNewArticles('republicans', 25, cursor, conn, 'hotArticles')
   
   
   
   
   