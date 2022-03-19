import csv
import requests
from bs4 import BeautifulSoup
import concurrent.futures as c

proxy_lst = []
#csv_path = './proxies.csv'
success_cnt = 0

def get_proxies():
    r = requests.get('https://free-proxy-list.net/')
    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find('tbody')
    proxies = []
    for row in table:
        if row.find_all('td')[4].text =='elite proxy':
            proxy = ':'.join([row.find_all('td')[0].text, row.find_all('td')[1].text])
            proxies.append(proxy)
        else:
            pass
    return proxies

# def get_proxy_lst(csv_path):
#     """ csv 파일에 있는 proxy를 proxy 리스트에 담아서 리턴하는 함수"""
#     with open(csv_path, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             proxy_lst.append(row[0])
#     return proxy_lst

def extract(proxy):
    """proxy를 추가해 GET 요청 후 응답을 받는 함수"""
    global success_cnt
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}
        page = requests.get('https://httpbin.org/ip', headers=headers, proxies={'http' : proxy,'https': proxy}, timeout=2)
        print(f"{page.json()} ' - {proxy} 성공")
        success_cnt += 1
    except:
        print("-" * 100)
        print(f"{proxy} 실패")
    return proxy


if __name__ == "__main__":

    proxy_lst = get_proxies()

    with c.ThreadPoolExecutor() as exe:
        exe.map(extract, proxy_lst)

    success_rate = success_cnt / len(proxy_lst) 
    print("-" * 100)
    print("success rate : {:.0%}".format(success_rate))