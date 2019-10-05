# -*- coding: UTF-8 -*-
import requests,os, random,urllib, time, sys,oauth2
import json

def login(username,password):
    session = requests.Session()
    session.headers = requests.utils.default_headers()
    session.headers.update({
                "Host": "www.instagram.com",
                "Origin": "https://www.instagram.com",
                "Referer": "https://www.instagram.com/",
                "X-Instagram-AJAX": "1",
                "X-Requested-With": "XMLHttpRequest",
            })

    cx = session.get("https://instagram.com")
    session.headers.update({'X-CSRFToken' :cx.cookies["csrftoken"]})
    data = {
                "username": username
                "password": password,
            }
    x = session.post("https://www.instagram.com/accounts/login/ajax/",data=data)
    session.headers.update({'X-CSRFToken' :x.cookies["csrftoken"]})
    likeurl = "https://www.instagram.com/web/likes/2147538068138459186/like/"

    s = session.post(likeurl)

username = ""
password = ""

login(username,password)
