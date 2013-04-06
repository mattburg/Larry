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


def scrapeNewArticles(subreddit):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   newSubmissions = r.get_subreddit(subreddit).get_new_by_date(limit=100)
   for thing in newSubmissions:
      #print thing.subreddit
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments]
      
      cursor.execute('INSERT OR REPLACE INTO newArticles values (?,?,?,?,?,?,?,?,?,?,?)', t)

      conn.commit()
      



 

if __name__ == "__main__":

    #dbPath="/Users/greg/Dropbox/research/crowdCuration/code/redditScraper/mydatabase.db"
   dbPath = "/Users/greg/localResearch/redditDB.db"
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

   #Put list of subreddits to be scraped here
   scrapeNewArticles('politics')
   scrapeNewArticles('worldnews')
   scrapeNewArticles('uspolitics')

   scrapeNewArticles('liberal')
   scrapeNewArticles('democrats')
   scrapeNewArticles('progressive')
   
   scrapeNewArticles('conservative')
   scrapeNewArticles('republicans')

