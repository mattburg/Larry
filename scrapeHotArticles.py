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

   dbPath="/Users/greg/localResearch/redditDB.db"
   
    #Dropbox/research/crowdCuration/code/redditScraper/mydatabase.db"

   conn = sqlite3.connect(dbPath)
   cursor = conn.cursor()
 
# create a table
   cursor.execute("""CREATE TABLE if not exists topArticles
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer) 
               """)
   cursor.execute("""CREATE TABLE if not exists newArticles
                  (id text PRIMARY KEY, subreddit text, dateCreated date, title text,  domain text, url text, author text,
                   score integer, ups integer, downs integer, numComments integer) 
               """)

   scrapeHotArticles('politics')
   scrapeHotArticles('worldnews')
   scrapeHotArticles('uspolitics')
   
   
   conn.commit()
   