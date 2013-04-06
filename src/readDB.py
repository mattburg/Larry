import sqlite3
from datetime import datetime
import praw


def getDate(sub_id):

   result = r.get_submission(submission_id = sub_id)
   return datetime.fromtimestamp(result.created)

#does a binary search to get the post closest to specified date
def getStartID(year, month, date):
   
   totalQuery = "SELECT COUNT(*) FROM sub_id";
   
   cursor.execute(totalQuery)
   
   totalRows = cursor.fetchone()[0]
   
   targetDate = datetime(year, month, date)
   
   print targetDate
   
   print totalRows
   print type(totalRows)
   
   cursor.execute("SELECT * FROM sub_id WHERE rowid = 1")
   result = cursor.fetchone()
   
   lowerBoundDate = getDate(result["id"])
   cursor.execute("SELECT * FROM sub_id WHERE rowid = (?)", [totalRows])
   result = cursor.fetchone()
   
   upperBoundDate = getDate(result["id"])
   
   print lowerBoundDate
   print upperBoundDate
   
   lowerIndex = 1
   upperIndex = totalRows
   lastID = 0
   lastRowID = 0
   while lowerIndex < upperIndex:
      currentIndex = (lowerIndex + upperIndex)/2
      
      cursor.execute("SELECT rowid, * FROM sub_id WHERE rowid = (?)", [currentIndex])
      result = cursor.fetchone()
      currentDate = getDate(result["id"])
      if currentDate == targetDate:
         return result["rowid"], result["id"]
      if currentDate < targetDate: 
         lowerIndex = currentIndex + 1
      if currentDate > targetDate:
         upperIndex = currentIndex - 1
         
      lastID = result["id"]
      lastRowID = result["rowid"]
      print "( " + str(lowerIndex) + ", " + str(upperIndex) + ")"
      
   print getDate(lastID)   
   print "row id " + str(lastRowID)
   return lastRowID, lastID
   

def scrapeUserNames():

   #startRowID, startID = getStartID(2009,1,1)
   startRowID = 1841957 # hard coded value for 2009-1-1
   offSet = 212856 #hard coded value for picking up scraping where it was left off
   startRowID += offSet
   #lastRowID, lastID = getStartID(2009,6,1)
   lastRowID = 2627858 #hard coded value for 2009-6-1
   cursor.execute("SELECT * FROM sub_id WHERE rowid >= (?) AND rowid <= (?)", [startRowID, lastRowID])
   results = cursor.fetchall()
   resultList = list(results)
   print len(resultList)
   submissionIDs = []
   for result in resultList:
      submissionIDs.append("t3_" + str(result["id"]))
      
   smallList =  submissionIDs[1:5000]   
   
   submissions = r.get_submissions(submissionIDs)
   numProcessed = 0
   for submission in submissions: 
   
      print submission.author
      cursor.execute("INSERT INTO userNames VALUES (?) ", [str(submission.author)])
      conn.commit()   
      numProcessed += 1
      print "Names processed : " + str(numProcessed)
         
def setupDB():
   
   global r
   r = praw.Reddit("test user agent")
   global conn
   dbPath = "/Users/greg/localResearch/idDB.db"
   conn = sqlite3.connect(dbPath)
   conn.row_factory = sqlite3.Row
   global cursor
   
   cursor = conn.cursor()
   cursor.execute("""CREATE TABLE if not exists sub_id
                  (id text)
                  """)
   cursor.execute("""CREATE TABLE if not exists userNames
                  (name text)
                  """)  
if __name__ == "__main__":

   dbPath = "localResearch/idDB.db"
   
   tempConn = sqlite3.connect(dbPath)
   cursor = tempConn.cursor()
   
             
   
   with open("scores.data") as infile:
      for line in infile:
         print line
         print line.split()[0]
         
         cursor.execute("INSERT INTO sub_id VALUES (?)", [line.split()[0]])
         conn.commit()
      #conn.commit()