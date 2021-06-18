# Instini

Instini is an http based Instagram bot.


## Features

The following code snippets should be edited in the quickstart file. <br>


#### Liking posts:
```python
#...
username = "" #your username
password = "" #your password


#grab posts from a tag
session.add_tags(["food","foodporn","travel"]) #your tags here

like = True
percent_to_like = 100   #percent of grabbed posts to like
#...
```


#### Commenting on posts:
```python
#...
username = "" #your username
password = "" #your password


#grab posts from a tag
session.add_tags(["food","foodporn","travel"]) #your tags here
#...
comment = True
percent_to_comment_on = 30 #percent of grabbed posts to comment on
#...
#your comments here
comments = ["nice","not bad","cool","don't care","amazing","unbelievable","Post more like this!","fire","looks good","f4f?","do you know any good hashtags for posts like this??"]
#...
```

