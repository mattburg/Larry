import sys
import praw
from datetime import datetime


def base36encode(number):
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    base36 = ''
    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or alphabet[0]

def base36decode(number):
    return int(number,36)


if __name__ == "__main__":

   print base36encode(325)
   x = base36encode(325)
   user_agent = "user name collector "
   r = praw.Reddit(user_agent=user_agent)
   firstSubmissionNumber = 325
   submission_ids = []
   for i in range(1,50):
      num = base36encode( firstSubmissionNumber + i )
      print num
      print "t3_" + str(num)
      submission_ids.append("t3_" + str(num))
   
   print submission_ids
   thing = r.get_submission(submission_id="flxzk")
   print thing
   myTime = datetime.fromtimestamp(thing.created)
   print myTime.strftime('%Y-%m-%d')
   print "length is " + str(len(submission_ids))
   results = r.get_submissions(submission_ids)
   for result in results:
      print result.id
      print result.title
      print result.created 
      subTime = datetime.fromtimestamp(result.created)
      print subTime.strftime('%Y-%m-%d')