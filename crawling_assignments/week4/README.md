```python
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
from dateutil.parser import parse
import pytz
```


```python
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
```


```python
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
```


```python
def get_post(driver):
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')

    info = {}

    try:
        contents = soup.select('div.MOdxS > span')[0].text,
    except:
        contents = None
    try:
        tags = clean_hashtag(soup.select('div.MOdxS > span')[0].text),
    except:
        tags = None
    try:
        # like가 0일 수는 있다.
        like = soup.select("div._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll > span")[0].text,
    except:
        like = 0
    try:
        created_at = convert_datetime(soup.select_one("time").get("datetime"))
    except Exception as e:
        created_at = None

    info['contents'] = contents[0] if type(contents) == tuple else contents
    info['tags'] = tags[0] if type(tags) == tuple else tags
    info["like"] =  like[0] if type(like) == tuple else like
    info["created_at"] = created_at

    return info
```


```python
def move_next(driver):
    # 다음 버튼을 클릭하기
    right = driver.find_element(By.CSS_SELECTOR, 'body > div.RnEpo._Yhr4 > div.Z2Inc._7c9RR > div > div.l8mY4.feth3 > button')
    right.click()
    time.sleep(4)
```


```python
s = Service(ChromeDriverManager().install())
o = webdriver.ChromeOptions()

# option을 설정하기 ( 크롬을 끈 상태로 진행한다. )
# o.add_argument('headless')

driver = webdriver.Chrome(service=s, options=o)

driver.get('https://www.instagram.com')

driver.maximize_window()
time.sleep(3)

id = "your id"
pw = "your password"

# facebook button
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

# 페이지 로딩 대기
time.sleep(5)

post = driver.find_elements(By.CSS_SELECTOR, "div.v1Nh3.kIKUG._bz0w")[0]
post.click()

max_post = 50
result = []

for i in range(max_post):
    data = get_post(driver)
    result.append(data)
    move_next(driver)

time.sleep(5)

# pandas
df = pd.DataFrame(result)
df.to_csv("./insta_data")
```

    
    
    ====== WebDriver manager ======
    Current google-chrome version is 99.0.4844
    Get LATEST chromedriver version for 99.0.4844 google-chrome
    Driver [C:\Users\l2t\.wdm\drivers\chromedriver\win32\99.0.4844.51\chromedriver.exe] found in cache
    

    로그인 성공
    


```python
df.tail(10)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>contents</th>
      <th>tags</th>
      <th>like</th>
      <th>created_at</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>40</th>
      <td>오늘은 판벌려녀의 쩝쩝일기어제 판벌려녀가 퇴근시간쯤에 나한테 까르보불닭이랑 꿀조합 ...</td>
      <td>None</td>
      <td>5</td>
      <td>2022-03-24T20:52:48+09:00</td>
    </tr>
    <tr>
      <th>41</th>
      <td>#닭꼬치 #맛집 #논현 #강남 #직화 #수제 ...</td>
      <td>[여자들이좋아하는술집, 맛집, 강남, 노...</td>
      <td>0</td>
      <td>2022-03-24T20:51:34+09:00</td>
    </tr>
    <tr>
      <th>42</th>
      <td>#출장#대구 출장왔는데 맛집이고 뭐고 퓌곤해서 포장해다가 호텔에서...그래도 납작만...</td>
      <td>[daily, 일상, 납작만두, 맛집, 월드컵예선, 맥주, 소통, 대한민국vs이란,...</td>
      <td>6</td>
      <td>2022-03-24T20:52:13+09:00</td>
    </tr>
    <tr>
      <th>43</th>
      <td>콩자반🦑...#07 #07년생 #instagood #더블글래스 #카페 #일상 #맛집...</td>
      <td>[더블글라스, 중딩스타그램, 맞팔환영, instagood, followforfoll...</td>
      <td>0</td>
      <td>2022-03-24T20:51:52+09:00</td>
    </tr>
    <tr>
      <th>44</th>
      <td>📍#삼미칼국수 #판교맛집판교 테크노벨리 삼환하이펙스에 있는 칼국수 맛집!💰#칼국수 ...</td>
      <td>[칼국수, 판교맛집판교, 삼미칼국수]</td>
      <td>27</td>
      <td>2022-03-24T20:52:05+09:00</td>
    </tr>
    <tr>
      <th>45</th>
      <td>#하루ㆍㆍ오예~ 선제골ㆍ대한민국 1:0 이란ㆍㆍㆍ#그냥다좋아서그램 #인스타그램 #일...</td>
      <td>[디엠, 외럽스타그램, 키작녀, 韓国人と繋がりたい, 솔로스타그램, いいです, 축구하...</td>
      <td>3</td>
      <td>2022-03-24T20:51:31+09:00</td>
    </tr>
    <tr>
      <th>46</th>
      <td>#샌드위치만들기ㅋㅋㅋ맛본빵만 몇개인지ㅎㅎㅎ#게살샌드위치😃여기가 샌드위치 맛집이네 🤭...</td>
      <td>[사직동, 샌드위치만들기ㅋㅋㅋ맛본빵만, 게살샌드위치😃여기가, 맛집, 부산]</td>
      <td>3</td>
      <td>2022-03-24T20:52:17+09:00</td>
    </tr>
    <tr>
      <th>47</th>
      <td>3년만인 규한이^^일본대학 간 사람이랑 중국대학 간 사람ㅋㅋㅋㅋ 한국 김치 많이 먹...</td>
      <td>[중국유학생, 맛집, 일본유학생, 명륜진사갈비, 먹스타그램]</td>
      <td>2</td>
      <td>2022-03-24T20:51:55+09:00</td>
    </tr>
    <tr>
      <th>48</th>
      <td>마포참치가 리뷰모음!고객님들의 만족 리뷰들 입니다!소중한 리뷰들이 힘든 이 시기를 ...</td>
      <td>None</td>
      <td>12</td>
      <td>2022-03-24T20:51:38+09:00</td>
    </tr>
    <tr>
      <th>49</th>
      <td>#마니산산채 부모님 모시고 다녀왔어요~ 너무 맛있다고 좋아하시고 아버지는 막걸리까지...</td>
      <td>[마니산산채, 일산맛집마니산산채, 프리미엄아울렛맛집, 파주한정식, 파주맛집, 일산여...</td>
      <td>0</td>
      <td>2022-03-24T20:51:52+09:00</td>
    </tr>
  </tbody>
</table>
</div>


