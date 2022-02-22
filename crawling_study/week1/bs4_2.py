# 신뢰성 있는 통신을 위한 예외 핸들링
from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError

from bs4 import BeautifulSoup

try:
    html = urlopen("https://www.pythonscraping.com/pages/warandpeace.html")
except HTTPError as e:
    print(e)
except URLError as e:
    print("서버를 찾을 수 없습니다.")
else:
    print("성공")

bs = BeautifulSoup(html, 'html.parser')

if __name__ == "__main__":
    # bs 객체가 존재하지 않는 태그에 접근할 수 있으므로 AttributeError 예외를 처리한다.
    try:
        bad_content = bs.non_existing_content.another_tag
        # good_content = bs.html
    except AttributeError as e:
        print("태그를 찾을 수 없습니다.")
    else:
        if not bad_content:
            print("태그를 찾을 수 없습니다.")
        else:
            print(bad_content)
    