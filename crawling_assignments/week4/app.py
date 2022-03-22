from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import config
import time
import pandas as pd
import re
from dateutil.parser import parse
import pytz
import os
from collections import defaultdict

def convert_datetime(s):
    #https://twpower.github.io/29-iso8601-utc-and-python-example
    #https://stackoverflow.com/questions/28949911/what-does-this-format-means-t000000-000z

    # ISO8601 포맷의 datetime 문자열을 python datetime으로 변환
    dt = parse(s)

    # Asia/Seoul Timezone 설정
    local_timezone = pytz.timezone("Asia/Seoul")

    # Timezone에 따라 새로운 date 형식을 변경
    local_date = dt.replace(tzinfo=pytz.utc).astimezone(local_timezone)

    # ex) 2022-03-21T21:32:12+09:00
    return local_date.isoformat()


def clean_hashtag(txt):

    tag_lst = re.findall(r'#[^\s]*', txt)
    temp_lst = []

    if not tag_lst:
        return None

    for s in tag_lst:
        if s.count("#") >= 2:

            temp_lst.extend(s.split('#')[1:])
        else:
            temp_lst.append(s.split('#')[-1])

    return list(set(temp_lst))


def get_post(driver):
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    info = {}

    try:
        info["contents"] = soup.select('div.MOdxS > span')[0].text,
    except:
        info["contents"] = None
    try:
        info["tags"] = clean_hashtag(soup.select('div.MOdxS > span')[0].text),
    except:
        info["tags"] = None
    try:
        # like가 0일 수는 있다.
        info["like"] = soup.select("div._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll > span")[0].text,
    except:
        info['like'] = 0
    try:
        info["created_at"] = convert_datetime(soup.select_one("time").get("datetime"))
    except:
        pass

    print(info)

    return info

def move_next(driver):
    # 다음 버튼을 클릭하기
    right = driver.find_element(By.CSS_SELECTOR, 'body > div.RnEpo._Yhr4 > div.Z2Inc._7c9RR > div > div.l8mY4.feth3 > button')
    right.click()
    time.sleep(4)



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
print("로그인 성공")

# 맛집 hashtag 찾기

url = "https://www.instagram.com/explore/tags/{}/".format("맛집")
driver.get(url)

# selenium wait for navigation 등의 method
# time.sleep을 대체할 수 있는 기능 찾아오기
#react-root > section > main > article > div.EZdmt > div > div > div:nth-child(1) > div:nth-child(1)

# 페이지 로딩 대기
time.sleep(5)

post = driver.find_elements(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")[0]
post.click()

max_post = 50
result = []

for i in range(max_post):
    print(i+1)
    data = get_post(driver)
    result.append(data)
    move_next(driver)

time.sleep(5)

# pandas

df = pd.DataFrame(result)
df.to_csv("./instragram_data")

