# -*- coding: UTF-8 -*-
import requests, os, random, urllib, time, sys
import json

def shortcode_to_id(shortcode):
        id = 0;
        alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_';
        for letter in shortcode:
                id = (id * 64) + alphabet.index(letter);
        return id;
  

class Instini(object):

        def __init__(self,username,password):
                self.username = username
                self.password = password
                self.logged_in = True

                self.post_queue = []
                
                self.base_url = "https://instagram.com"
                self.like_url = "https://www.instagram.com/web/likes/{0}/like/"
                self.login_url = "https://www.instagram.com/accounts/login/ajax/"
                self.media_url = "https://www.instagram.com/p/{0}"
                self.logout_url = "https://www.instagram.com/accounts/logout/"
                self.comment_url = "https://www.instagram.com/web/comments/{0}/add/"
                self.explore_url = "https://www.instagram.com/explore/tags/{0}/"
                
                self.session = requests.Session()
                self.init_session()
                
                self.login(username,password)
                
        def add_tags(self,tags):
                for tag in tags:
                        explore_response = self.session.get(self.explore_url.format(tag))
                        if explore_response:
                                explore_page = explore_response.content
                                for line in explore_page.split(b'\n'):
                                        if b'sharedData = {"config' in line:
                                                #line = line.split(b" = ")[1][:-10].replace(b"\\\\",b"")
                                                try:
                                                    line = line.split(b" = ")[1]
                                                    page = json.loads(line[:line.rfind(b";<")].replace(b"\\\\",b""))
                                                except:
                                                    print(line)
                                                    print(b";</script" in line);self.logout();exit()
                                                    print("Explore page error, exiting")
                                                    self.logout()
                                                    exit()
                                                pagecount = 1
                                                posts = []
                                                for i in range(pagecount):
                                                    posts.extend(page["entry_data"]["TagPage"][i]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"])
                                                print("Found {0} posts ".format(len(posts)))
                                                for post in posts:
                                                    self.post_queue.append(post["node"])
                                                break
                
        def init_session(self):
                self.session.headers = requests.utils.default_headers()
                self.session.headers.update({
                        "User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:69.0) Gecko/20100101 Firefox/69.0",
                        "Host": "www.instagram.com",
                        "Accept": "*/*",
                        "Accept-Language": "en-US,en;q=0.5",
                        "Accept-Encoding": "gzip, deflate, br",
                        "DNT": "1",
                        "Connection": "keep-alive",
                        "Pragma": "no-cache",
                        "Cache-Control": "no-cache",
                        "TE": "Trailers",
                        "Origin": self.base_url,
                        "Referer": self.base_url,
                        "X-Instagram-AJAX": "1",
                        "X-Requested-With": "XMLHttpRequest",
                })
    
                #send dummy request to get initial csrf token
                cx = self.session.get(self.base_url)
                self.session.headers.update({'X-CSRFToken' :cx.cookies["csrftoken"]})
                
        def login(self,username,password):
                
                data = {"username": username,"password": password}
                                
                login_response = self.session.post(self.login_url,data=data)
                try:
                    success = json.loads(login_response.content)["authenticated"]
                except:
                    success = False

                if success:
                        print("Login successful")
                        self.logged_in = True
                else:
                        try:
                            login_json = json.loads(login_response.content)
                            failed = login_json["status"] == "fail"
                        except:
                            failed = False

                        if(failed):
                            print("Login failed, {0}".format(login_json["message"].lower()))
                        else:
                            print("Login failed, check credentials")

                        #print(login_response.content)
                        exit()
                
                self.session.headers.update({'X-CSRFToken' :login_response.cookies["csrftoken"]})

        def logout(self):
                logout_response = self.session.post(self.logout_url)
                
                if logout_response:
                        print("Logout successful")
                else:
                        print("Logout failed")

        def like_media(self,url):
                s = self.session.post(url)
                try:
                    success = (json.loads(s.content)["status"] == "ok")
                except:
                    success = False
                return success

        def comment_media(self,url,comment):
            data = {"comment_text":comment,"replied_to_comment_id":None}
            s = self.session.post(url,data=data)
            try:
                success = (json.loads(s.content)["status"] == "ok")
            except:
                print(s.content)
                success = False
            return success

        def like_from_queue(self):
            count = 1
            for post in self.post_queue:
                url = session.like_url.format(post["id"])
                direct_url = session.media_url.format(post["shortcode"])
                if(self.like_media(url)):
                    logstr = "Liked post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue))
                else:
                    logstr = "ERROR: Failed to like post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue))
                count += 1
                print("="*len(logstr))
                print(logstr)
                print("="*len(logstr))
                print()
                time.sleep(5)

username = ""
password = ""

session = Instini(username,password)
session.add_tags(["food"])
url = session.like_url.format(session.post_queue[-1]["id"])
print("Liking {0}".format(session.media_url.format(session.post_queue[-1]["shortcode"])))
#print(session.comment_media(url,"test comment"))
print("Like succeeded? {0}".format(str(session.like_media(url))))
#session.like_from_queue()
session.logout()
