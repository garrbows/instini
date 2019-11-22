from fake_useragent import UserAgent
import random

ua = UserAgent()

for i in range(100):
    print(ua.random)
