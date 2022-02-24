# 1주차 과제

### 당근마켓 중고상품정보 크롤링 

- 타겟 URL: https://www.daangn.com/hot_articles
- 과제 요구사항

    - HTTP 통신을 위해 [requests](https://docs.python-requests.org/en/latest/) 라이브러리를 설치한다.
        
        ```
        pip install requests
        ```

    - 원하는 정보를 `Parsing` 하기 위해 [Beautifulsoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) 라이브러리를 설치한다.  

        ```
        pip install beautifulsoup4
        ```
    - 당근마켓 서버에 `GET` 요청을 보내 중고상품정보를 전달받는다.
    
        먼저 간단하게 http 테스트를 위해 `httpie`를 설치하여 Target URL에 `GET` 요청을 보낸 후 응답메세지를 확인해보자
        
            
            # sudo apt install httpie # ubuntu일 경우
            http -v GET "https://www.daangn.com/hot_articles"
            
        HTTP 메세지는 서버와 클라이언트 간에 데이터가 교환되는 방식이다. 클라이언트는 서버에 `GET` 요청을 전달하여 서버로 부터 액션이 일어나게 하고 서버로부터 응답메시지를 전달받을 수 있다.

        
        <div align='center' style="margin: 30px 0px">
            <img src='./static/image/img_week1_1.png'/>
        </div>

        HTTP 메시지 구조에 대한 자세한 설명은 https://developer.mozilla.org/ko/docs/Web/HTTP/Messages 를 참고하자

    - 중고상품 페이지를 크롤링할때  로그인은 필요없으므로 `GET` 요청만 보내면 정보를 받아올 수 있다.

        ```
        webpage = requests.get("webpage = requests.get("https://www.daangn.com/hot_articles"))
        ```

        - webpage는 `Response` 객체이고 이 객체로부터 원하는 정보를 가져올 수 있다.

        - 객체는 `HTTP 요청`에 대한 서버의 응답이며 다음과 같이 다양한 기능을 사용할 수 있다.

        <div align='center' style="margin: 30px 0px">
            <img src='./static/image/img_week1_2.png'/>
        </div>
        
        References: [Python requests.Response Object](https://www.w3schools.com/python/ref_requests_response.asp), [Response content](https://docs.python-requests.org/en/latest/user/quickstart/)

    - 서버로부터 응답받은 `webpage` 객체와 `html.parser` 를 사용해 Beautifulsoup 객체를 생성한다.

        ```
        soup = BeautifulSoup(webpage.content, "html.parser")
        ```

        - webpage.content에는 직렬화된 byte 코드가 담겨있고 `html.parser`를 이용해 구문을 분석하여 문서화된 Beautifulsoup 객체를 생성할 수있다.
        
        <br>

        ```
        print(webpage.content)
        
        b'<!DOCTYPE html>\n<html lang="ko">\n<head>\n  <meta charset="utf-8">\n  <meta http-equiv="X-UA-Compatible" content="IE=edge">\n  <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
        ```

    - `BeautifulSoup`에는 [SoupSieve](https://facelessuser.github.io/soupsieve/) 패키지를 사용하여 구문 분석된 문서에 대해 `CSS Selector`를 실행하고 일치하는 모든 요소를 반환하는 `select` 메서드를 사용할 수 있다.

        ```
        # 사용예시
        soup.select("title")
        # [<title>The Dormouse's story</title>]

        soup.select("p:nth-of-type(3)")
        # [<p class="story">...</p>]
        ```

        - Return 타입은 요소가 하나일 경우 `bs4.element.Tag` 객체를 반환하며 2개 이상일 경우 내부 원소가 `Tag` 로 구성된 `list` 를 반환한다.  
        - `Beautifulsoup`는 HTML 문서를 파이썬 객체의 복잡한 트리로 변환하며 4가지 객체(`Tag` , `NavigableString`, `BeautifulSoup`, `Comment`를 사용할 수 있다.
        
        <br>

        ```
        # tag 객체 사용예시
        
        soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
        tag = soup.b
        type(tag)
        
        # <class 'bs4.element.Tag'>

        # Name
        tag.name
        # 'b'

        # Attributes
        tag['class]
        # 'boldest'

        tag.attrs
        # {'class': 'boldest'}

        ```

    - `cards-wrap` 태그 아래의 모든 `article` 을 가져오고 반환된 `getItem` 은 `iterable`한 list 이므로 반복문을 통해 `Tag` 객체의 `.select()`를 사용해 원하는 정보를 `Parsing` 할 수 있다. 

        ```
        # article 정보를 담을 리스트
        article_info_list = []

        for i, info in enumerate(articles):

            # article 각각의 정보를 담을 딕셔너리
            article_info_dict = {}
            article_info_dict["id"] = i + 1 # 상품ID
            article_info_dict["desc"] = info.select("a > div.card-desc > h2")[0].text.strip() # 상품설명
            article_info_dict["price"] = info.select("a > div.card-desc > div.card-price")[0].text.strip() # 상품가격
            article_info_dict["region_name"] = info.select("a > div.card-desc > div.card-region-name")[0].text.strip() # 지역명
            article_info_dict["interest"] = info.select("a > div.card-desc > div.card-counts")[0].text.split()[1] #관심
            article_info_dict["chatting"] = info.select("a > div.card-desc > div.card-counts")[0].text.split()[-1] # 채팅
            article_info_dict["img_url"] = info.select("a > div.card-photo > img")[0]["src"] # 이미지경로
            article_info_list.append(article_info_dict)

        print(article_info_list)
        ```

### 결과

<div align='center' style="margin-top:20px">
    <img src='./static/image/img_week1_3.png'/>
</div>


