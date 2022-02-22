# bs4_2 코드 리팩토링

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def get_title(url: str):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bs = BeautifulSoup(html, 'html.parser')
        title = bs.body.h1
    except AttributeError as e:
        return None
    return title

if __name__ == "__main__":
    url = "https://www.pythonscraping.com/pages/page1.html"
    title = get_title(url)

    # 제목이 존재하지 않는다면
    if not title:
        print("제목이 존재하지 않습니다")
    else:
        print(title.contents) # <h1>An Interesting Title</h1>