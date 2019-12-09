from instini import Instini

#==============
# CONFIG START
#==============

username = ""
password = ""

#grabs ~70 posts from each tag
tags = ["food","foodporn","travel"]

like = True
percent_to_like = 100   #percent of grabbed posts to like
comment = False
percent_to_comment_on = 30 #percent of grabbed posts to comment on

'''
WARNING
Letting bot comment without sufficient
comment options can get your account
flagged for suspicious activity. Use at
least 10 different comments.
'''

comments = ["nice","not bad","cool","don't care","amazing","unbelievable","Post more like this!","fire","looks good","f4f?","do you know any good hashtags for posts like this??"]


#==============
#  CONFIG END
#==============

if comment == True and len(comments) < 10:
    print("Insufficient comment options, add more comments")
    exit()

session = Instini(username,password)

session.add_tags(tags)

#Advanced users only
session.interaction_delay = 200                 #Delay after each interaction
session.interation_random_interval_max = 100    #Maximum random delay (added to each interaction)
session.interaction_reset = 500                 #Delay after receiving timeout

if like:
    session.like_from_queue(percent_to_like)
if comment:
    session.comment_from_queue(percent_to_comment_on)

if like or comment:
    session.interact_from_queue()

print("Session finished, exiting.")
