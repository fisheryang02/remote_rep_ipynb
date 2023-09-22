import time
from selenium import webdriver

browser = webdriver.Edge()
browser.get('https://www.baidu.com')
print(browser.page_source)
x=input()
browser.close()