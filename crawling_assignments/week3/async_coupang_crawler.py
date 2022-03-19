from requests_html import AsyncHTMLSession
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import asyncio
import time

urls = []
headers = { 
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'
}
item_list = []
sucess_cnt = 0
keyword = input()
for n in range(1,27):
    urls.append(f"https://www.coupang.com/np/search?q={keyword}&channel=user&component=&page={n}")

async def extract(s, url):

    try:
        res =  await s.get(url, headers=headers, timeout=5)
    except Exception as e:
        raise e
    
    global sucess_cnt

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

            # time.sleep(0.1)

    sucess_cnt += 1

    print(f"[{sucess_cnt} / 26] page success") 


async def work(urls):
    s = AsyncHTMLSession()
    tasks = (extract(s, url) for url in urls)
    return await asyncio.gather(*tasks)

if __name__ == "__main__":
    # 비동기 세션 관리 
    start = time.perf_counter()
    asyncio.run(work(urls))
    end = time.perf_counter()

    print(f"process time: {end - start} seconds")