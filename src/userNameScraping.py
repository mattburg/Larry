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

  
   
 
if __name__ == "__main__":

   conn = sqlite3.connect("mydatabase.db")
   cursor = conn.cursor()
 
# create a table
   cursor.execute("""CREATE TABLE if not exists userNames
                  (name text PRIMARY KEY, dumb text) 
               """)



   user_agent = "user name collector "
   r = praw.Reddit(user_agent=user_agent)
   
   allComments = r.get_all_comments(limit=1000)
   names = []
   for c in allComments:
      if( isinstance(c, praw.objects.Comment) == True):
         print c.author
         cursor.execute("INSERT OR REPLACE INTO userNames VALUES (?,?)", (str(c.author), 'x' ) )
         names.append(c.author)
   conn.commit()
   
   print "number of names is " + str(len(names))
   
   #newSubmissions = r.get_subreddit('all').get_new_by_date(limit=1000)
   #hotSubmissions = r.get_subreddit('all').get_hot(limit=10)
   #topSubmissions = r.get_subreddit('all').get_top(limit=10)
   #print "top submissions"
   #for thing in hotSubmissions:
      #t = str(thing.author)
      #print t
      #cursor.execute("INSERT OR REPLACE INTO userNames VALUES (?,?)", (str(thing.author), 'x' ) )
      
      #comments = thing.comments
      #for c in comments:
      #   if(isinstance(c, praw.objects.Comment) == True):
      #      cursor.execute("INSERT OR REPLACE INTO userNames VALUES (?,?)", (str(c.author), 'x' ) )
      
      
      #conn.commit()
   
