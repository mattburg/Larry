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
import datetime


import praw


def scrapeNewArticles(subreddit):
   conn = sqlite3.connect("mydatabase.db")
   cursor = conn.cursor()
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   newSubmissions = r.get_subreddit('politics').get_new(limit=100)
   for thing in newSubmissions:
      print thing.subreddit
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments]
      
      cursor.execute('INSERT OR REPLACE INTO newArticles values (?,?,?,?,?,?,?,?,?,?,?)', t)

      conn.commit()

def scrapeNewArticles(subreddit, articleLimit, cursor, conn, tableName):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   newSubmissions = r.get_subreddit(subreddit).get_new(limit=articleLimit)
   print "new submissions"
   for thing in newSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments,datetime.datetime.now()]
      
      cursor.execute('INSERT OR REPLACE INTO ' + str(tableName) + '   values (?,?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit() 


def scrapeNewArticlesPositionDependent(subreddit, articleLimit, cursor, conn, tableName):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   newSubmissions = r.get_subreddit(subreddit).get_new(limit=articleLimit)
   print "new submissions"
   position = 1
   for thing in newSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, 
            thing.num_comments,datetime.datetime.now(), position]
      position += 1
      
      cursor.execute('INSERT INTO ' + str(tableName) + '   values (?,?,?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit() 

      
def scrapeHotArticles(subreddit):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   hotSubmissions = r.get_subreddit(subreddit).get_hot(limit=25)
   print "top submissions"
   for thing in hotSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments]
      
      cursor.execute('INSERT OR REPLACE INTO topArticles values (?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit()
      

      
def scrapeHotArticles(subreddit, articleLimit, cursor, conn, tableName):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   hotSubmissions = r.get_subreddit(subreddit).get_hot(limit=articleLimit)
   print "hot submissions"
   for thing in hotSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments,datetime.datetime.now()]
      
      cursor.execute('INSERT OR REPLACE INTO ' + str(tableName) + '   values (?,?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit()  
      
def scrapeHotArticlesPositionDependent(subreddit, articleLimit, cursor, conn, tableName):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   hotSubmissions = r.get_subreddit(subreddit).get_hot(limit=articleLimit)
   print "hot submissions"
   position = 1
   for thing in hotSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, 
            thing.num_comments,datetime.datetime.now(), position]
      position += 1
      cursor.execute('INSERT INTO ' + str(tableName) + '   values (?,?,?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit()    
      
def scrapeTopArticles(subreddit, articleLimit, cursor, conn, tableName):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   topSubmissions = r.get_subreddit(subreddit).get_top(limit=articleLimit)
   print "top submissions"
   for thing in topSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, thing.num_comments]
      
      cursor.execute('INSERT OR REPLACE INTO trainingData values (?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit()


#Need to make sure there's not a primary key on article ID       
def scrapeTopArticlesPositionDependent(subreddit, articleLimit, cursor, conn, tableName):
   user_agent = "political bias scaper"
   r = praw.Reddit(user_agent=user_agent)
   topSubmissions = r.get_subreddit(subreddit).get_top(limit=articleLimit)
   print "top submissions"
   position = 1
   for thing in topSubmissions:
      print thing

      
      t = [thing.id, str(thing.subreddit), thing.created, thing.title, 
            thing.domain, thing.url, str(thing.author), thing.score, thing.ups, thing.downs, 
            thing.num_comments, position]
      position += 1
      cursor.execute('INSERT INTO trainingData values (?,?,?,?,?,?,?,?,?,?,?)', t) 
      conn.commit()

def main(user, thing_type="submissions"):
   thing_limit = RETRIEVE_LIMIT
   user = r.get_redditor(user)
   gen = (user.get_comments(limit=thing_limit) if thing_type == "comments" else
          user.get_submitted(limit=thing_limit))
   for thing in gen:
       subreddit = thing.subreddit.display_name
       print thing.score
       karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) 
                                        + thing.ups - thing.downs)
   submissions = r.get_subreddit('python').get_top(limit=10)
 

if __name__ == "__main__":

   conn = sqlite3.connect("mydatabase.db")
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

   scrapeNewArticles('politics')
   scrapeTopArticles('politics')
