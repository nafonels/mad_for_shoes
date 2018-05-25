from bs4 import BeautifulSoup
import requests
import urllib.request as req
import datetime
import json
import matplotlib.pyplot as plt
import matplotlib
import pytagcloud
import webbrowser
from matplotlib import font_manager, rc
from itertools import count
from collections import OrderedDict
from selenium import webdriver
from urllib import parse
from konlpy.tag import Twitter
from collections import Counter
import re

search_url="https://search.naver.com/search.naver"
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

    response = requests.get(search_url, params = param, headers = hrd)
    web_soup = BeautifulSoup(response.text, 'html.parser')
    area = web_soup.find("div", {"class" : "blog section _blogBase"}).find_all("a", {"class" : "url"})
    
    for tag in area:
        url1=tag.get('href')
        print("{:} {:}".format(cnt,url1))
        
        if tag['href'] in post_dict:                #해당 url이 이미 post_dict 변수에 존재하면 마지막이라는 의미
            print("마지막 페이지 마지막블로그 입니다 링크추출을 종료합니다")
            exit()                                #종료
        
        post_dict[tag['href']] = tag.text       # url값과 태그내용으로 post_dict 딕셔너리에 저장
        cnt +=1

        
    def redirect_naverblog(url) -> str:
        splited_url = parse.urlparse(url)

        if splited_url.netloc == 'blog.naver.com':
            if splited_url.path == '/PostView.nhn':  # blog.naver.com/PostView.nhn?blogId=<account>&logNo=<post_id>
                query_string = parse.parse_qs(splited_url.query)
                ret = _reparse_url(query_string['blogId'], query_string['logNo'])

            elif splited_url.path.count('/') > 2:  # blog.naver.com/<account>/<post_id>
                query_string = splited_url.path.split('/')
                ret = _reparse_url(*query_string[-2:])

            else:  # blog.naver.com/<account>?logNo=<post_id>
                query_string = (splited_url.path[1:],
                *parse.parse_qs(splited_url.query)['logNo'])
                ret = _reparse_url(*query_string)
    
    url="https://blog.naver.com/PostView.nhn?blogId=sinsils&logNo=221221464708&redirect=Dlog&widgetTypeCall=true&directAccess=false"
    res = req.urlopen(url)
    soup = BeautifulSoup(res, 'html.parser')
    print(soup)

    soup = BeautifulSoup(res, 'html.parser')
    title = soup.findAll("span", {"class":"pcol1 itemSubjectBoldfont"})
    
    wd = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
    wd.get("{:}".format(url1))
#     wd.execute_script("")
    html = wd.page_source
    print(html)

    for a in title:            
        print(a)
        print(a.get_text())
