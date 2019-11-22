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
                self.logged_in = False

                self.filters = {}
                self.post_queue = []
                f = open("ua.txt","r")
                self.ualist = f.readlines()
                f.close()

                self.dolike = False
                self.like_percent = 0
                self.docomment = True
                self.comment_percent = 0
                self.comment_list = []
                
                self.base_url = "https://instagram.com"
                self.user_url = "https://instagram.com/{0}"
                self.like_url = "https://www.instagram.com/web/likes/{0}/like/"
                self.login_url = "https://www.instagram.com/accounts/login/ajax/"
                self.media_url = "https://www.instagram.com/p/{0}"
                #needs username, query string __a for image index in story
                self.story_url = "https://www.instagram.com/stories/{0}/?" 
                self.story_watch_url = "https://www.instagram.com/stories/reel/seen/"
                self.follow_url = "https://www.instagram.com/web/friendships/{0}/follow/"
                self.graphql_url = "https://www.instagram.com/graphql/query/{0}"
                self_unfollow_url = "https://www.instagram.com/web/friendships/{0}/unfollow/"
                self.logout_url = "https://www.instagram.com/accounts/logout/"
                self.comment_url = "https://www.instagram.com/web/comments/{0}/add/"
                self.explore_url = "https://www.instagram.com/explore/tags/{0}/"
                
                self.session = requests.Session()
                self.init_session()
                
                self.login(username,password)

                self.interaction_delay = 20
                self.interaction_reset = 100

                f = open("ua.txt","r")
                self.ualist = f.readlines()
                f.close()

        def get_random_ua(self):
            return random.choice(self.ualist).replace("\n","")

        def get_page_data(self,url):
            page_response = self.session.get(url)
            if page_response:
                page = page_response.content
                for line in page.split(b'\n'):
                    if b'sharedData = {"config' in line:
                        try:
                            line = line[line.find(b"{"):line.rfind(b"}")+1]
                            page_data = json.loads(line)
                        except:
                            print(line)
                            print(b";</script" in line);self.logout();exit()
                            print("Explore page error, exiting")
                            self.logout()
                            exit()
                self.set_csrf_token_from(page_response)
                return page_data
                
        def add_tags(self,tags):
                for tag in tags:
                        page = self.get_page_data(self.explore_url.format(tag))
                        pagecount = 1
                        posts = []
                        for i in range(pagecount):
                            posts.extend(page["entry_data"]["TagPage"][i]["graphql"]["hashtag"]["edge_hashtag_to_media"]["edges"])
                            print("Found {0} posts ".format(len(posts)))
                        for post in posts:
                            self.post_queue.append(post["node"])

        def set_csrf_token_from(self,response):
            try:
                self.session.headers.update({'X-CSRFToken' :response.cookies["csrftoken"]})
            except:
                print()

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
                self.set_csrf_token_from(cx)
                
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
                
                self.set_csrf_token_from(login_response)

        def logout(self):
                logout_response = self.session.post(self.logout_url)
                
                if logout_response:
                        print("Logout successful")
                else:
                        print("Logout failed")

        def get_user_id(self,url):
            profile_response = self.get_page_data(url)
            if profile_response:
                userid = profile_response["entry_data"]["ProfilePage"][0]["graphql"]["user"]["id"]
            else:
                print("ERROR: Failed to retrieve profile page")
                userid = 0
            return userid

        def get_username_from_id(self,userid):
            return self.graphql_query("user",userid)

        #query type, aux data (user id,etc.)
        def graphql_query(self,t,data):
            typedict = {"user":"?query_hash=aec5501414615eca36a9acf075655b1e&variables=%7B%22user_id%22%3A%22{0}%22%2C%22include_chaining%22%3Atrue%2C%22include_reel%22%3Atrue%2C%22include_suggested_users%22%3Afalse%2C%22include_logged_out_extras%22%3Afalse%2C%22include_highlight_reels%22%3Atrue%7D"
                    }
            if t not in typedict.keys():
                print("Query type {0} not found".format(t))
                return ""
            url = self.graphql_url.format(typedict[t].format(data))
            graphql_response = self.session.get(url)
            if graphql_response:
                if t == "user":
                    return json.loads(graphql_response.content)["data"]["user"]["reel"]["owner"]["username"]

        def follow_user(self,userid):
            url = self.follow_url.format(userid)

            s = self.session.post(url)
            try:
                success = (json.loads(s.content)["result"] == "following")
            except:
                success = False
                f = open("t.html","wb+")
                f.write(s.content)
                f.close()
            return success

        def like_media(self,url):
            s = self.session.post(url)
            try:
                success = (json.loads(s.content)["status"] == "ok")
            except:
                success = False
            self.set_csrf_token_from(s)
            return success

        def comment_media(self,url,comment):
            data = {"comment_text":comment,"replied_to_comment_id":None}
            s = self.session.post(url,data=data)
            try:
                success = (json.loads(s.content)["status"] == "ok")
            except:
                print(s.content)
                success = False
            self.set_csrf_token_from(s)
            return success

        def like_from_queue(self,percent=100):
            self.like_percent = percent
            self.dolike = True

        def comment_from_queue(self,commentList,percent=100):
            self.comment_list = commentList
            self.comment_percent = percent
            self.docomment = True
        
        def interact_from_queue(self):
            count = 1
            do_like = False
            do_comment = False
            print("\nInteracting with {0} posts with following rules:".format(len(self.post_queue)))
            if(self.dolike):
                print("\tLike {0}% of posts".format(self.like_percent))
            if(self.docomment):
                print("\tComment on {0}% of posts".format(self.comment_percent))
                print("\n\t==================\n\tComment selection: \n\t"+"\n\t".join(self.comment_list)+"\n\t==================\n")
            checked = []
            for i in range(len(self.post_queue)):
                post = random.choice(self.post_queue)
                while post in checked:
                    post = random.choice(self.post_queue)
                checked.append(post)
                com_url = session.comment_url.format(post["id"])
                l_url = session.like_url.format(post["id"])
                direct_url = session.media_url.format(post["shortcode"])
                if(self.like_from_queue):
                    do_like = random.randrange(0,100) <= self.like_percent
                if(self.comment_from_queue):
                    do_comment = random.randrange(0,100) <= self.comment_percent

                if(not (do_comment or do_like)):
                    print("Skipping post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue)))
                    count  += 1
                    continue
                logstr = ""
                if(do_comment):
                    comment = random.choice(self.comment_list)
                    if(self.comment_media(com_url,comment)):
                        logstr += "Commented '{3}' on post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue),comment)
                    else:
                        logstr += "ERROR: Failed to comment '{3}' on post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue),comment)
                        print("Sleeping for "+str(self.interaction_reset)+" seconds to reset interaction cooldown")
                        time.sleep(self.interaction_reset)
                if(do_like):
                    if(self.like_media(l_url)):
                        logstr += "\nLiked post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue))
                    else:
                        logstr += "\nERROR: Failed to like post ({1}/{2}): {0}".format(direct_url,count,len(self.post_queue))
                        print("Sleeping for "+str(self.interaction_reset)+" seconds to reset interaction cooldown")
                        time.sleep(self.interaction_reset)
                count += 1
                if "\n" in logstr:
                    if logstr[0] == "\n":
                        logstr = logstr[1:]
                        print("="*len(logstr))
                        print(logstr)
                        print("="*len(logstr))
                    else:
                        print("="*len(logstr.split("\n")[1]))
                        print(logstr)
                        print("="*len(logstr.split("\n")[1]))
                else:
                    print("="*len(logstr))
                    print(logstr)
                    print("="*len(logstr))
                print()
                f = open("log.txt","a+")
                f.write(logstr+"\n")
                f.close()
                time.sleep(self.interaction_delay)

        def get_post_time(self,post):
            return post["taken_at_timestamp"]
        def get_poster_id(self,post):
            return post["owner"]
        def post_older_than(self,post,seconds):
            return self.get_post_time(post) <= time.time() - seconds
        def get_followers(self,username):
            data = self.get_page_data(self.user_url.format(username))
            try:
                return int(data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_followed_by"]["count"])
            except:
                print("Error fetching profile data")
                return ""
        def poster_has_followers(self,username,count):
            return self.get_followers(username) >= count

        def start(self):
            self.interact_from_queue()

        def get_stories(self,username):
            has_highlights = has_story = False
            data = self.get_page_data(self.user_url.format(username))
            #fetch stories
            if(len(data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]) > 0):
                has_story = True
                story_ids = [i["node"]["id"] for i in data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]]
                story_times = [i["node"]["taken_at_timestamp"] for i in data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"]]
                #story_reel_id = ["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_owner_to_timeline_media"]["edges"][0]["node"]["owner"]["id"]
                userid = self.get_user_id(self.user_url.format(username))
            #fetch highlights
            if(int(data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["highlight_reel_count"]) > 0):
                has_highlights = True
                highlight_ids = [i["node"]["id"] for i in data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_felix_video_timeline"]["edges"]]
                highlight_times = [i["node"]["taken_at_timestamp"] for i in data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_felix_video_timeline"]["edges"]]
                try:
                    highlight_reel_id = data["entry_data"]["ProfilePage"][0]["graphql"]["user"]["edge_felix_video_timeline"]["edges"][0]["node"]["owner"]["id"]
                except:
                    highlight_reel_id = ""
            else:
                hightlight_ids = hightlight_times = []
                highlight_reel_id = 0
            stories = []
            if has_story:
                for i in range(len(story_ids)):
                    stories.append(
                    {
                      "reelMediaId":str(story_ids[i]),
                      "reelMediaOwnerId":str(userid),
                      "reelId":str(userid),
                      "reelMediaTakenAt":str(story_times[i]),
                      "viewSeenAt":str(9999999999)
                    })
            if has_highlights:
                for i in range(len(highlight_ids)):
                    stories.append(
                    { 
                      "reelMediaId":str(highlight_ids[i]),
                      "reelMediaOwnerId":str(userid),
                      "reelId":"highlight:"+str(highlight_ids[i]),
                      "reelMediaTakenAt":str(highlight_times[i]),
                      "viewSeenAt":str(9999999999)
                    })
            return stories

