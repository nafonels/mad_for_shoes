from selenium import webdriver
wd = webdriver.Chrome('C:/chromedriver_win32/chromedriver.exe')
wd.get('https://www.facebook.com/shoeswhat/?_fb_noscript=1')
wd.execute_script("?_fb_noscript=1#")
html = wd.page_source
print(html)
