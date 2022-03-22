from bs4 import BeautifulSoup
import re
from dateutil.parser import parse
import pytz


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

lst = []

with open('./post_html.txt', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), features='lxml')
    

    di = {}
    di["contents"] = soup.select('div.MOdxS > span')[0].text,
    di["tags"] = clean_hashtag(soup.select('div.MOdxS > span')[0].text),
    di['like'] = soup.select("div._7UhW9.xLCgt.qyrsm.KV-D4.fDxYl.T0kll > span")[0].text,
    di['created_at'] = convert_datetime(soup.select("time")[0].get("datetime"))
    
    print(di)

import pandas as pd
df = pd.DataFrame(di)

print(df)
