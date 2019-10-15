# Instini

Instini is an http based instagram bot.


## Features

#### Liking posts:
```python
username = ""   #your username here
password = ""   #your password here

#create instini session
session = Instini(username,password)

#grab images from a tag
session.add_tags(["food"])

#like the first post you grabbed
url = session.like_url.format(session.post_queue[0]["id"])
print("Liking {0}".format(session.media_url.format(session.post_queue[0]["shortcode"])))
print("Like succeeded? {0}".format(str(session.like_media(url))))

#end session
session.logout()
```


#### Commenting on posts:
```python
username = ""   #your username here
password = ""   #your password here

#create instini session
session = Instini(username,password)

#grab images from a tag
session.add_tags(["food"])

comment = "test comment" #insert your comment here

#like the first post you grabbed
url = session.comment_url.format(session.post_queue[0]["id"])
print("Commenting '{1}' on {0}".format(session.media_url.format(session.post_queue[0]["shortcode"]),comment))
print("Comment succeeded? {0}".format(str(session.comment_media(url,comment))))

#end session
session.logout()
```

