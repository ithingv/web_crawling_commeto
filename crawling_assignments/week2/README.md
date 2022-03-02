# 모듈 


```python
import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin
```

# 크롤링 페이지 범위 설정


```python
keyword = input("검색어: ")

url = "https://www.coupang.com/np/search"

headers = { 
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

params = {
    'component': '',
    'q': keyword,
    'channel': 'user',
    'page': 1
}

# 첫번째 페이지
try:
    res =  requests.get(url, params=params, headers=headers, timeout=5)
except TimeoutError as e:
    raise TimeoutError("Timeout Error")

if res.status_code == 200:
    soup = BeautifulSoup(res.content, "html.parser")
    last_page = int(soup.select_one('a.btn-last').text.strip())

last_page = int(last_page)
print(f"상품 {keyword}의 마지막 페이지는 {last_page} 입니다.")
```

    검색어: 콜라
    상품 콜라의 마지막 페이지는 27 입니다.
    

# 여러 페이지 크롤링
---

- 크롤링 페이지 범위 1 ~ last_page


- Time interval 설정(Optional)
    
    - 0초 ~ 1초 사이
    - round(random.random(), 1)


```python
# Target URL
url = "https://www.coupang.com/np/search"

# 검색할 키워드
keyword = input("검색어: ")

# 브라우저가 요청하는 것 처럼 동작하기 위해 header를 설정한다.
# Network 탭의 패킷에서 'User-Agent'를 확인
headers = { 
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}

# 결과 저장할 리스트
item_list = []

# 콜라 키워드의 쿠팡 페이지를 크롤링
for idx in range(last_page):
    params = {
        'component': '',
        'q': keyword,
        'channel': 'user',
        'page': idx + 1
    }

    try:
        res =  requests.get(url, params=params, headers=headers, timeout=5)
    except TimeoutError as e:
        raise TimeoutError("Timeout Error")

    if res.status_code == 200: # 서버로부터 정상적으로 응답을 받았다면
        soup = BeautifulSoup(res.content, 'html.parser')
        get_item = soup.select('ul#productList li')
        
        for item in get_item:
            """
            name: 상품명
            price: 상품가격
            item_link: 상품과 연결된 URL주소
            discount_rate: 할인율(1~100%, 할인이 없는 경우 '할인안함'으로 저장)
            item_point: 상품점수 (점수가 없는 경우 '없음'으로 저장)
            """
            item_info = {}
            item_info['name'] = item.select_one('div.name').text.strip()
            item_info['price'] = item.select_one('strong.price-value').text.strip().replace(',', '')
            item_info['item_link'] = urljoin("https://www.coupange.com/", item.select_one('a').get('href'))

            try:
                item_info['discount_rate'] = item.select_one('span.instant-discount-rate').text.strip() 
            except AttributeError:
                item_info['discount_rate'] = '할인안함'

            try:
                item_info['item_point'] = item.select_one('em.rating').text.strip()
            except AttributeError:
                item_info['item_point'] = '없음'

            item_list.append(item_info)
            
#             Optional 
#             0 ~ 1 sec, time sleep
#             interval = round(random.random(), 1)
#             time.sleep(interval)
```

    검색어: 콜라
    


```python
# 크롤링한 상품개수
len(item_list)
```




    936



# 크롤링 결과 저장

- pandas DataFrame 사용
- 엑셀로 저장


```python
import pandas as pd
result_df = pd.DataFrame(item_list)
```


```python
result_df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>name</th>
      <th>price</th>
      <th>item_link</th>
      <th>discount_rate</th>
      <th>item_point</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>펩시 콜라, 250ml, 30개</td>
      <td>20500</td>
      <td>https://www.coupange.com/vp/products/393818?it...</td>
      <td>1%</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>[코카콜라음료] 코카콜라 190ml x, 60캔</td>
      <td>30430</td>
      <td>https://www.coupange.com/vp/products/618419122...</td>
      <td>할인안함</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>롯데 칠성사이다 355ml캔 24개입(업소용), 상세페이지 참조</td>
      <td>20100</td>
      <td>https://www.coupange.com/vp/products/630483894...</td>
      <td>할인안함</td>
      <td>4.5</td>
    </tr>
    <tr>
      <th>3</th>
      <td>코카콜라, 185ml, 30개</td>
      <td>16770</td>
      <td>https://www.coupange.com/vp/products/107307587...</td>
      <td>할인안함</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>*콤부차 마스크팩 증정 * 아임얼라이브 유기농 콤부차 10병(PET), 오리지널</td>
      <td>36000</td>
      <td>https://www.coupange.com/vp/products/606055717...</td>
      <td>5%</td>
      <td>5.0</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>931</th>
      <td>숨겨진 맥주 캔 상자 병 콜라 유리 음료 홀더 단열 가방 캠핑 액세서리 여행 하이킹...</td>
      <td>27700</td>
      <td>https://www.coupange.com/vp/products/637118571...</td>
      <td>할인안함</td>
      <td>없음</td>
    </tr>
    <tr>
      <th>932</th>
      <td>Mini Mobile Phone 1.0인치 블루투스 호환 듀얼 SIM 콜라 모양 포...</td>
      <td>42880</td>
      <td>https://www.coupange.com/vp/products/635276516...</td>
      <td>45%</td>
      <td>없음</td>
    </tr>
    <tr>
      <th>933</th>
      <td>[바보사랑] 스텐실 도안(ST-4034) 코카콜라모음-사이즈별, 상세 설명 참조</td>
      <td>5400</td>
      <td>https://www.coupange.com/vp/products/190967916...</td>
      <td>할인안함</td>
      <td>없음</td>
    </tr>
    <tr>
      <th>934</th>
      <td>콜라상회 패브릭 포스터 태피스트리, 홀리데이 바나나 리프</td>
      <td>10900</td>
      <td>https://www.coupange.com/vp/products/140420973...</td>
      <td>할인안함</td>
      <td>4.0</td>
    </tr>
    <tr>
      <th>935</th>
      <td>롯데칠성음료 펩시 제로 콜라 슈가 라임 190ml 30개, 상세페이지 참조</td>
      <td>16750</td>
      <td>https://www.coupange.com/vp/products/583841296...</td>
      <td>할인안함</td>
      <td>5.0</td>
    </tr>
  </tbody>
</table>
<p>936 rows × 5 columns</p>
</div>




```python
# 엑셀 파일로 저장
# result_df.to_excel("coupang_crawling_result.xlsx")
```


```python
# csv 파일로 저장
result_df.to_csv('coupang_crawling_result.csv', encoding='utf-8', index=False)
```
