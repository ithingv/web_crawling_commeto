# requests BeautifulSoup
import requests
# bs4 에서 BeautifulSoup을 가져왔다 Import
from bs4 import BeautifulSoup
# for 문 돌리기 - 반복문
# range => 범위 range(100) 0~99 숫자 백개
# range(n) 0 ~ n-1 숫자 n개
# index 0~ n~1
# for 문이 한번 진행될때마다 index +1
# for문은 range의 숫자가 다끝나면 n-1까지 돌아가면 종료
for index in range(5):
    page = index+1
    params = {
    "component": "",
    "q": "콜라",
    "channel": "user",
    "page": page
    }

#
 # component:
 # q: % EB % 83 % 89 % EC % 9E % A5 % EA % B3 % A0
 # channel: user
try:
    webpage = requests.get("https://www.coupang.com/np/search", params=params, timeout=5)
except TimeoutError:
    raise TimeoutError("time out error")

soup = BeautifulSoup(webpage.content, "html.parser")
 # 상품 상세
 # #\35 109971962 > a > dl > dd > div
 # ul => li class search-product search-product__ad-badge => a => div class

#descriptions-inner
getItem = soup.select(
 # "#productList > li.search-product > a > dl.search-product-wrap > dd.descriptions
#> div.descriptions-inner")
 # 이런식으로 크롤링이 안되는 경우에는 위에서 부터 찾아서
 # select_one이라는 메소드로 직접 찾아간다.
# 실행이 안될 겁니다.
# 이처럼 크롤링이 너무 많이 들어올땐 요청한 request의 헤더를 확인합니다. 브라우저의 정보를 보고 정보가 없으면 아예 접근하지 못
# 하게 막아버릴 수도 있습니다.
# 이럴때는 우리 프로그램 자체도 브라우저인척 변장을 해야됩니다.
# 크롤링이 접근이 안될때!
# 브라우저를 똑같이 따라하자
 "ul#productList li")

base_url = 'https://coupang.com'

for item in getItem:
    item_name = item.select_one('div.name').text.strip()
    item_price = item.select_one('strong.price-value').text.strip().replace(',', '')
    item_link = base_url + item.select_one('a').get('href')
    check_item_discount_rate = item.select_one('span.instant-discount-rate')
    item_discount_rate = '할인 안함'
 # 할인을 안하는 경우 None이 나와서 에러가 난다.
 # 이럴때는 html이 규칙적이지 않다는 건데
 # if 라는 조건문을 통해서 할인이 있는 경우만 가져오면 에러가 나지 않는다.
    if check_item_discount_rate:
        item_discount_rate = check_item_discount_rate.text.strip()
        check_item_point = item.select_one('em.rating')
        item_point = '없음'
 
    if check_item_point:
        item_point = item.select_one('em.rating').text.strip()
        print(item_name)
        print(item_price)
        print(item_discount_rate)
        print(item_link)
        print(item_point + '점')