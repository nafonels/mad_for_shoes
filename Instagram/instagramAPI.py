## pip install python-instagram 로 설치
# from selenium import webdriver
# wd = webdriver.Chrome("C:/Python36/WebDriver/chromedriver.exe")
# wd.get("https://www.instagram.com/")

import urllib.request
from bs4 import BeautifulSoup

html = urllib.request.urlopen("https://www.instagram.com/")
soup = BeautifulSoup(html, 'html.parser')

end_cursor
:
"AQALNaPide91cdrwXQxqt9IfLsLxzk8m5nbCth9nz8AJ1XHnH_mWk5N6WCq4rg22gVp5XVIh_TxOkyJE6AgsPIgaC_scn09JpGe9dPw9b55HTg"


import InstaPy

InstaPy(username='test', password='test')\
  .login()\
  .set_do_comment(True, percentage=10)\
  .set_comments(['Cool!', 'Awesome!', 'Nice!'])\
  .set_dont_include(['friend1', 'friend2', 'friend3'])\
  .set_dont_like(['food', 'girl', 'hot'])\
  .set_ignore_if_contains(['pizza'])\
  .like_by_tags(['dog', '#cat'], amount=100)\
  .end()

import InstaPy
# [ 로그인 ]
session = InstaPy(username='test', password='test')
session.login()
# [ 항목별 데이터 수집 ]
session.like_by_tags(['#dog', 'cat'], amount=100)
session.like_by_locations(['26429/chrysler-building/', '224442573/salton-sea/'], amount=100)
session.like_from_image(url='www.instagram.com/p/BSrfITEFUAM/', amount=100)
session.like_from_image(amount=100)

session.like_by_tags(['#animals'], amount=50, media='Photo')
session.like_from_image(url='www.instagram.com/image', amount=50, media='Photo')
session.like_by_tags(['#cat'], amount=15, media='Video')
session.like_from_image(url='www.instagram.com/image', amount=15, media='Video')

session.end()
