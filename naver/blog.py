from bs4 import BeautifulSoup
import requests
import urllib.request as req
import datetime
from itertools import count
from collections import OrderedDict
from selenium import webdriver
import re

url="https://search.naver.com/search.naver"
hrd = {"User-Agent": "Mozillg/5.0" , "referer" : "http://naver.com"}

post_dict = OrderedDict()
cnt = 1
for page in count(1,1):
    param = {
        "where" : "post",
        "query" : "신발",
        "date_from" : "20170515",
        "date_to" : "20180515",
        "date_option" : 7,
        "start" : (page-1) * 10 + 1
        }

    response = requests.get(url, params = param, headers = hrd)
    soup = BeautifulSoup(response.text, 'html.parser')
    area = soup.find("div", {"class" : "blog section _blogBase"}).find_all("a", {"class" : "url"})
    
    for tag in area:
        url1=tag.get('href')
        print("{:} {:}".format(cnt,url1))
        
        if tag['href'] in post_dict:                #해당 url이 이미 post_dict 변수에 존재하면 마지막이라는 의미
            print("마지막 페이지 마지막블로그 입니다 링크추출을 종료합니다")
            exit()                                #종료
        
        post_dict[tag['href']] = tag.text       # url값과 태그내용으로 post_dict 딕셔너리에 저장
        cnt +=1
        
    wd = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
    wd.get("{:}".format(url1))
#     wd.execute_script("")
    html = wd.page_source
    print(html)
    

# for tag in area:
#     url1 = tag.get('href')
#     print("{:}".format(url1))
# print(response)
# print(response.url)
# print(response.status_code)
# print(response.text)