from bs4 import BeautifulSoup
import requests
import urllib.request as req
import datetime
import json
import sys
import urllib.request
from itertools import count
from collections import OrderedDict
from urllib import parse
from selenium import webdriver
import re
 
def redirect_naverblog(url) -> str:
    # 최종 목표는
    # blog.naver.com/PostView.nhn?blogId=gkdbf32&amp;logNo=221279336454
    # 의 형식으로 url을 변환하는 것
    splited_url = parse.urlparse(url)

    ret: str
    # host가 blog.naver.com인 경우
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
 
    # host가 <name>.blog.me인 경우
    else:
        query_string = (splited_url.netloc.split('.')[0],
                        splited_url.path[1:])
        ret = _reparse_url(*query_string)
    return parse.urljoin(url, '//' + ret)

def _reparse_url(blogid, post_no):
    url = f"blog.naver.com/PostView.nhn?blogId={blogid}&logNo={post_no}"
    return url

search_url="https://search.naver.com/search.naver"
hrd = {"User-Agent": "Mozillg/5.0" , "referer" : "http://naver.com"}

post_dict = OrderedDict()
cnt = 1
dictionary = []
jsonResult = []
wd = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
for page in count(1,1):#count(1,1):
    param = {
        "where" : "post",
        "query" : "휠라 디스럽터2",
        "date_from" : "20170525",
        "date_to" : "20180524",
        "date_option" : 7,
        "start" : (page-1) * 10 + 1
        }

    response = requests.get(search_url, params = param, headers = hrd)
    web_soup = BeautifulSoup(response.text, 'html.parser')
    area = web_soup.find("div", {"class" : "blog section _blogBase"}).find_all("a", {"class" : "url"})
    
    for tag in area:
        url1=tag.get('href')
        url = redirect_naverblog(url1)
        print("{:} {:} {:}".format(cnt,url1,url))
        
        if tag['href'] in post_dict:                #해당 url이 이미 post_dict 변수에 존재하면 마지막이라는 의미
            print("마지막 페이지 마지막블로그 입니다 링크추출을 종료합니다")
            exit()                                #종료
        
        post_dict[tag['href']] = tag.text       # url값과 태그내용으로 post_dict 딕셔너리에 저장
        cnt +=1

#     url="https://blog.naver.com/PostView.nhn?blogId=llmement&logNo=221253993406"
        try:
            wd.get("{:}".format(url))
            html = wd.page_source
        except:
            print('포스트가 삭제되었습니다.')
            continue
        
    
    #     res = req.urlopen(url)
        soup = BeautifulSoup(html, 'html.parser')
    #     soup = BeautifulSoup(res, 'html.parser')
    #     print(soup)
        try:
            title = soup.select(".pcol1 > .se_editArea")[0].get_text()
            a = soup.select('.view')[0].get_text()
            b = soup.select('.post_commentview_btn > a > em')[0].get_text()
            c = soup.select('.u_cnt')[0].get_text()
        except:
            print('리스트가 비어었습니다.')
        print(title)
        print(a)
        print(b)
        print(c)

        text={}
        text['title'] = title
        text['post'] = a
        text['comment_cnt'] = b
        text['like_cnt'] = c
        print(text)
        dictionary.append(text)
        
        with open('disruptor2.json', 'w', encoding = 'utf8')as outfile:
            str_ = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        print('disruptor2.json SAVED')


    #     wd.get("{:}".format(url1))
    #     wd.execute_script("")
    #     html = wd.page_source
    #     print(html)
    # 
    #     for a in title:            
    #         print(a)
    #         print(a.get_text())