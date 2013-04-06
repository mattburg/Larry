#!/usr/bin/env python


import argparse
import operator
import sys
import urllib2
import sqlite3

import praw


def main(user, thing_type="submissions"):
   """
   Create a dictionary with karma breakdown by subreddit.
      
   Takes a user and a thing_type (either 'submissions' or 'comments') 
   as input. Return a directory where the keys are display names of 
   subreddits, like proper or python, and the values are how much 
   karma the user has gained in that subreddit.
   """
   RETRIEVE_LIMIT = 100
   karma_by_subreddit = {}
   thing_limit = RETRIEVE_LIMIT
   user = r.get_redditor(user)
   print user
   gen = (user.get_comments(limit=thing_limit) if thing_type == "comments" else
          user.get_submitted(limit=thing_limit))
   for thing in gen:
       subreddit = thing.subreddit.display_name
       print thing.score
       karma_by_subreddit[subreddit] = (karma_by_subreddit.get(subreddit, 0) 
                                        + thing.ups - thing.downs)
    
   for thing in gen: 
      print thing.subreddit.display_name
   return karma_by_subreddit

if __name__ == "__main__":

   conn = sqlite3.connect("mydatabase.db")
   cursor = conn.cursor()
 
# create a table
   cursor.execute("""CREATE TABLE if not exists userSubmissions
                  (id text PRIMARY KEY, 
                  author text, 
                  dateCreated date, 
                  title text, 
                  subreddit text, 
                  score integer,
                  ups integer, 
                  downs integer, 
                  numComments integer)
                  """)

   cursor.execute("""CREATE TABLE if not exists userComments
                  (id text PRIMARY KEY, 
                  author text, 
                  dateCreated date,  
                  subreddit text, 
                  score integer,
                  ups integer,
                  downs integer,
                  numReplies integer)
                  """)   



   user_agent = "user post success predictor"
   r = praw.Reddit(user_agent=user_agent)
   user = r.get_redditor("thisaintnogame")
   allSubmissions = user.get_submitted() #this gets all the posts a user has made
   
   for thing in allSubmissions:
      print thing.author
      print thing
      print thing.subreddit
      print thing.score
      thing.replace_more_comments()
      submissionComments = thing.comments
      print len(submissionComments)
      #print thing.
      # cursor.execute("INSERT OR REPLACE INTO userSubmissions VALUES (?,?,?,?,?,?,?,?,?)",
#                      (thing.id,
#                      str(thing.author),
#                      thing.created,
#                      thing.title,
#                      thing.subreddit.display_name,
#                      thing.score))
#       
#       conn.commit()
      #print vars(thing)  
    
    
   allComments = user.get_comments()   
   for comment in allComments: 
      if comment.is_root == False:
         continue
      print comment.author
      print comment
      print comment.subreddit
      print comment.score
      commentReplies = comment.replies
      print "Number of replies = " + str(len(commentReplies))
      
      
      
      
      
      
      
      
      
      
      
      
      
      
      