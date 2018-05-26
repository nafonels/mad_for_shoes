#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from itertools import count
from urllib import parse

import requests
from bs4 import BeautifulSoup, NavigableString
from selenium import webdriver

from setting import chromedriver
from util.iofunc import save_json
from util.logger import logger


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


def search(keyword, date_to = "20170501"):
    search_url = "https://search.naver.com/search.naver"
    hrd = {"User-Agent": "Mozillg/5.0", "referer": "http://naver.com"}

    post_dict = {}
    cnt = count(1)

    json_post = []
    json_media = []
    is_final = False

    wd = webdriver.Chrome(chromedriver)
    for page in count(1, 1):
        # blog search & pagination
        param = {
            "where":       "post",
            "query":       keyword,
            "date_from":   date_to,
            "date_to":     "20180524",
            "date_option": 7,
            "start":       (page - 1) * 10 + 1
        }

        response = requests.get(search_url, params = param, headers = hrd)
        web_soup = BeautifulSoup(response.text, 'html.parser')

        # get blog page url
        area = web_soup.find("div", {"class": "blog section _blogBase"}).find_all("a", {"class": "url"})

        for tag in area:
            if is_final:
                break

            old_url = tag.get('href')

            if old_url in post_dict:  # 해당 url이 이미 post_dict 변수에 존재하면 마지막이라는 의미
                logger.info("마지막 페이지 마지막블로그 입니다 링크추출을 종료합니다")
                is_final = True
                break

            url_host = parse.urlsplit(old_url)

            logger.debug("{:} {:}".format(next(cnt), old_url))

            if url_host.netloc == 'blog.naver.com':
                url = redirect_naverblog(old_url)
            elif '.'.join(url_host.netloc.split('.')[-2:]) == 'blog.me':
                url = redirect_naverblog(old_url)

            else:
                try:
                    blog_res = requests.get(old_url)
                    url = BeautifulSoup(blog_res.text, 'html.parser').find('frame').get('src')
                    url = redirect_naverblog(url)
                except:
                    logger.warn(f'warnBlogType: {old_url} is not naver blog.')
                    continue
            logger.debug(f'- new url : {url}')
            post_dict[old_url] = tag.text  # url값과 태그내용으로 post_dict 딕셔너리에 저장

            try:
                wd.get(url)
                time.sleep(1)
                html = wd.page_source

            except:
                print('포스트가 삭제되었습니다.')
                continue

            #     res = req.urlopen(url)
            soup = BeautifulSoup(html, 'html.parser')
            #     soup = BeautifulSoup(res, 'html.parser')
            #     print(soup)

            post_page = soup.select('table#printPost1 table.post-top')
            if not post_page:
                title = soup.select(".pcol1 h3")[0].text.strip()
                post_date = soup.select('span.se_publishDate')[0].text.strip()
                post = soup.select('div.sect_dsc')[0]

            else:
                title = soup.select('div#title_1 > span.pcol1')
                print(title)
                title = title.pop().text  # .strip()
                post_date = soup.select('p.date')[0].text.strip()
                post = soup.select('div#postViewArea > div')[0]

            hash_tag = soup.select('div.post_footer_contents > div')[0]
            if isinstance(hash_tag.next, NavigableString):
                hash_tag = ''
            else:
                hash_tag = ' '.join(x.text for x in (*hash_tag.children,)[1:])

            comment = soup.select('.post_commentview_btn > a')
            if len(comment):
                comment = comment[0]

                comment_cnt = comment.select('em')
                if len(comment_cnt):
                    comment_cnt = comment_cnt[0].get_text()
                else:
                    comment_cnt = 0

            else:
                comment_cnt = 0

            like_cnt = soup.select('.u_cnt')
            if len(like_cnt):
                like_cnt = like_cnt[0].get_text()
            else:
                like_cnt = 0

            # 다음과 같이 클릭을 전달할 수 있다.
            # wd.find_element_by_css_selector('.post_commentview_btn > a').click()
            # time.sleep(3)

            # print()
            custom_post = {}
            custom_post['post_id'] = '_'.join(['naver', ] +
                                              parse.parse_qs(parse.urlsplit(url).query)['logNo'])
            custom_post['title'] = title
            custom_post['post_date'] = post_date
            custom_post['post'] = post.text.strip()
            custom_post['hash_tag'] = hash_tag
            custom_post['comment_cnt'] = int(comment_cnt)
            custom_post['like_cnt'] = int(like_cnt)
            custom_post['url'] = url
            # print(custom_post)
            json_post.append(custom_post)

            for img in post.find_all('img'):
                custom_media = {}
                # print(dir(img))
                custom_media['post_id'] = custom_post['post_id']
                custom_media['file_url'] = img.attrs['src']
                if parse.urlsplit(custom_media['file_url']).netloc == 'postfiles.pstatic.net':
                    a = parse.urlparse(custom_media['file_url'])
                    b = parse.parse_qs(a.query)  # type : dict
                    b.pop('type')

                    a = list(a)
                    a[4] = parse.urlencode(b)
                    custom_media['file_url'] = parse.urlunparse(a)
                custom_media['file_name'] = parse.urlsplit(custom_media['file_url']).path.split(r'/')[-1]
                # print(custom_media)
                json_media.append(custom_media)

            # for video

            # just for debug
            # exit(0)
        if is_final:
            break
    save_json('naver', keyword, 'post', json_post)
    save_json('naver', keyword, 'media', json_media)

    logger.info('disruptor2 SAVED')


search("디스럽터2")
search("에어맥스97")
