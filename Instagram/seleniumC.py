# [ IMPORT ] #

from selenium import webdriver
import time


# [ 검색 ]
driver = webdriver.Chrome("C:/Python36/WebDriver/chromedriver.exe")
driver.get("https://www.instagram.com/explore/tags/%s/" %("신발"))

# [ 스크롤 내리기 (방법1) ]
i = 0
while i < 8: #스크롤 횟수 설정
    i = i+1
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

# [ 스크롤 내리기 (방법2) ]
no_of_pagedowns = 10  # 스크롤 횟수 설정
while no_of_pagedowns:
    elem.send_keys(Keys.PAGE_DOWN)
    time.sleep(0.2)
    no_of_pagedowns -= 1

# [ Network 데이터를 못받아 올 경우 f5 누르기]
driver.refresh()



# todo: pagedown을 4~5회 전달
# todo: ajax 요청하는 내용을 우리가 받아볼 수 있어야 한다. 날아가는 것을 우리가 알 수 있는지 확인





# username = input("Input ID : ")  # User ID
# password = getpass.getpass("Input PWD : ")  # User PWD
# hashTag = input("Input HashTag # : ")  # Search #

# [ HASHTAG USING CHECK ] #

# if checkTag == -1:
#     hashTag = '#' + hashTag

# [ Login ] #
#
# element_id = driver.find_element_by_name("username")
# element_id.send_keys(username)
# element_password = driver.find_element_by_name("password")
# element_password.send_keys(password)
#
# password = 0  # RESET Password
#
# element_password.submit()

# [ LOGIN COMPLETE and SEARCH ] #

# elem = driver.find_element_by_name("_eduze _mknn3 ")
# elem.send_keys("신발")
# elem.send_keys(Keys.ENTER)
# driver.findElement(By.ClassName("_avvq0 _o716c")).sendKeys("Hey!");


#
#
# driver.find_element_by_xpath(
# "//div[@class='_5ayw3 _ohiyl']/input[@class='_avvq0 _o716c'].value").send_keys('신발')
# driver.find_element_by_xpath(
# "//div[@class='_dv59m']/a[@class='_ndl3t  _4jr79']").click()
#
# searchTotalCount = driver.find_element_by_xpath(
# """//*[@id="react-root"]/section/main/article/header/span/span""").text
# print('검색결과  Total : ' + searchTotalCount + ' 건 의 게시물이 검색되었습니다.')
#
# elem = driver.find_element_by_tag_name("body")
#
# time.sleep(1)
#
elem = driver.find_element_by_tag_name("body")

# [ AUTO PAGE DOWN ] #
# 자동으로 스크롤을 두번 내려줌
# no_of_pagedowns = 2


# while no_of_pagedowns:
#     elem.send_keys(Keys.PAGE_DOWN)
#     time.sleep(0.5)
#     no_of_pagedowns -= 1

# provider_elems = driver.find_elements_by_class_name("className")
#
# for post in provider_elems:
#     print(post.text)
