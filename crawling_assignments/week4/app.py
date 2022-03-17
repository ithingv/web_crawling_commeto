from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import config
import time
import pandas as pd

def get_post(driver):
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    try:
        # 안에 있는 내용 가져오기
        content = soup.select("div.C4VMK > span")[0].text
        print(content)
    except:
        content = ''

s = Service(ChromeDriverManager().install())
o = webdriver.ChromeOptions()

# option을 설정하기 ( 크롬을 끈 상태로 진행한다. )
# o.add_argument('headless')

driver = webdriver.Chrome(service=s, options=o)

driver.get('https://www.instagram.com')

driver.maximize_window()
time.sleep(3)

id = config.id 
pw = config.pw

# facebook button
# <span class="KPnG0">Facebook으로 로그인</span>
fb_btn = driver.find_element(By.CLASS_NAME, "KPnG0")
fb_btn.click()

input_id = driver.find_element(By.ID, 'email')
input_pw = driver.find_element(By.ID, 'pass')

input_id.send_keys(id)
input_pw.send_keys(pw)

time.sleep(1)

login_btn = driver.find_element(By.ID, 'loginbutton')
login_btn.click()


time.sleep(10)
print("login success")
# 맛집 hashtag 찾기

url = "https://www.instagram.com/explore/tags/{}/".format("맛집")
driver.get(url)

# selenium wait for navigation 등의 method
# time.sleep을 대체할 수 있는 기능 찾아오기
#react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1)
print(driver.find_element(By.CSS_SELECTOR, "div.eLAPa"))
# _elements(By.CSS_NAME, "div.v1Nh3.kIKUG._bz0w"))
# post.click()

# get_post(driver)

# max_post = 50
# result = []

# for i in range(max_post):
#     data = get_post(driver)
#     result.append(data)
#     # move_next(driver)