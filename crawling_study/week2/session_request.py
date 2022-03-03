from urllib import request
import requests

# 테스트용 httpbin.org
session = requests.Session()

# cookie
res1 = session.get("https://httpbin.org/cookies", cookies={"id": "ithingv"})
print(res1.text)

# 쿠키 set
res2 = session.get("https://httpbin.org/cookies/set", cookies={"id": "ithingv"})
print(res2.text)

# User-Agent
url = "https://httpbin.org"
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62"
}

res3 = requests.get(url, headers=headers)
print(res3.text)

session.close()

# with문 -> 파일, DB, HTTP
with requests.Session() as s:
    r = s.get("https://www.naver.com")
    print(r.text)
    print(r.ok)