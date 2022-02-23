from typing import List
import requests
from bs4 import BeautifulSoup
from util.calc import calc_time


@calc_time
def crawler(url: str) -> List:

    try:
        # 당근마켓 서버에 GET 요청을 보내고 데이터를 응답받음, timeout은 5초 제한
        res = requests.get(url, timeout=5.0)
    except requests.exceptions.RequestException as e:

        # https://www.codegrepper.com/code-examples/typescript/multiple+python+requests+timeout+exception
        # There was an ambiguous exception that occurred while handling your request
        raise SystemExit(e)
    try:
        # Beautifulsoup 객체 생성
        soup = BeautifulSoup(res.content, "html.parser")
        # 종고상품 정보를 parsing
        articles = soup.select("#content > section.cards-wrap > article")
    except AttributeError as e:
        raise AttributeError("not existing tag")

    # article 정보를 담을 리스트
    article_info_list = []

    for i, info in enumerate(articles):

        # article 각각의 정보를 담을 딕셔너리
        article_info_dict = {}
        article_info_dict["id"] = i + 1
        article_info_dict["desc"] = info.select("a > div.card-desc > h2")[0].text.strip()
        article_info_dict["price"] = info.select("a > div.card-desc > div.card-price")[0].text.strip()
        article_info_dict["region_name"] = info.select("a > div.card-desc > div.card-region-name")[0].text.strip()
        article_info_dict["interests"] = info.select("a > div.card-desc > div.card-counts")[0].text.split()[1]
        article_info_dict["comment_count"] = info.select("a > div.card-desc > div.card-counts")[0].text.split()[-1]
        article_info_dict["img_url"] = info.select("a > div.card-photo > img")[0]["src"]
        article_info_list.append(article_info_dict)

    return article_info_list
