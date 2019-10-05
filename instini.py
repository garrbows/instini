# -*- coding: UTF-8 -*-
import requests,os, random,urllib, time, sys
import json

class Instini(object):

	def __init__(self,username,password):
		self.username = username
		self.password = password
		
		self.base_url = "https://instagram.com"
		self.like_url = "https://www.instagram.com/web/likes/{0}/like/"
		self.login_url = "https://www.instagram.com/accounts/login/ajax/"
		self.logout_url = "https://www.instagram.com/accounts/logout/"
		
		self.session = requests.Session()		
		self.init_session()
		
		self.login(username,password)
		
	def init_session(self):
		self.session.headers = requests.utils.default_headers()
		self.session.headers.update({
			"Host": "www.instagram.com",
			"Origin": self.base_url,
			"Referer": self.base_url,
			"X-Instagram-AJAX": "1",
			"X-Requested-With": "XMLHttpRequest",
		})

		#send dummy request to get session cookie
		cx = self.session.get(self.base_url)
		self.session.headers.update({'X-CSRFToken' :cx.cookies["csrftoken"]})
		
	def login(self,username,password):
		
		data = {
					"username": username,
					"password": password,
				}
				
		x = self.session.post(self.login_url,data=data)
		self.session.headers.update({'X-CSRFToken' :x.cookies["csrftoken"]})

	def logout(self):
		logout_response = self.session.post(self.logout_url)
		
		if logout:
			print("Logout successful")
		else:
			print("Login successful")

	def like_media(self,url):
		s = self.session.post(url)
		if s:
			print("Like successful")
		else:
			print("Like failed")

username = ""
password = ""

session = Instini(username,password)
session.like_media("https://www.instagram.com/web/likes/2147599755135753945/like/")
session.logout()