# Free fake API for testing and prototyping.
# https://jsonplaceholder.typicode.com/

# json 데이터 10개 요청
# https://httpbin.org/stream/10

import json
import requests

res = requests.get("https://httpbin.org/stream/10", stream=True)

if res.encoding is None:
    res.encoding = 'UTF-8'

# Encoding 확인
print("Encoding: {}".format(res.encoding))

for line in res.iter_lines(decode_unicode=True):
    print(line)
    print(type(line))

    # JSON 변환 후 타입 확인 
    data = json.loads(line) # str -> dict
    
    for key, val in data.items():
        print("Key: {}, Value: {}".format(key, val))

    print("-"*100)



# header 정보
print(res.headers)

# 본문 정보
print(res.text)

# json 변환
print(res.json())