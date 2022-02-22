## 브라우저의 동작 원리

HTTP는 Hyper Text Transfer Protocol인데, Hyper Text를 전송하기 위한 프로토콜이라 할 수 있다.

클라이언트가 요청을 보내면 서버가 해당 요청에 대한 응답을 보내는 방식이며 데이터를 패킷으로 전송한다.

서버는 응답을 보내고 클라이언트와 연결을 바로 끊으며 통신이 끊기며 서버와 클라이언트는 무상태(stateless)를 유지한다.


1. 브라우저가 서버로부터 HTML, CSS, JavaScript, 이미지 파일을 응답받는다.
   - 웹 브라우저의 URL을 이용해 DNS 서버로 접근해 해당 도메인 네임에 맞는 IP를 검색한다
   - 요청을 위한 HTTP 메시지를 만든다.
   - 웹 브라우저와 서버가 TCP 3 way handshaking 방식으로 연결한다.
   - 웹 브라우저가 서버에 HTTP 요청을 보내고, 서버는 받은 HTTP 메시지를 해석해 리소스를 찾아 다시 브라우저로 전송한다.
   - 서버는 웹 브라우저와 TCP 4 way handshaking으로 연결을 해제한다.
   - 이미지를 받은 웹 브라우저는 이미지를 띄워 사용자에게 보여준다.

2. HTML, CSS 파일은 렌더링 엔진의 html parser와 css parser에 의해 파싱되며 DOM, CSSOM 트리로 변환되고 렌더 트리로 결합된다.
    - 렌더링이랑 개발자가 작성한 문자를 브라우저에서 그래픽 형태로 출력하는 것을 말한다.

3. HTML 파서는 script 태그를 만나면 자바스크립트 코드를 실행하기 위해 DOM 생성 프로세스를 중지하고 자바스크립트 엔진으로 제어 권한을 넘긴다.

4. 권한을 넘겨받은 자바스크립트 엔진은 script 태그 내의 자바스크립트 코드 또는 script 태그의 src attribute에 정의된 자바스크립트 파일을 로드하고 파싱해 실행한다.

5. 실행이 완료되면 다시 HTML 파서로 제어 권한을 넘겨서 DOM 생성을 재개한다.

6. 이 렌더 트리를 기반으로 웹페이지를 표시한다.


## 에러 핸들링

HTTPError
- 페이지를 찾을 수 없거나, URL 해석에서 에러가 생기는 경우 `404 Error`
- 서버를 찾을 수 없는 경우 `500 Error`
  
  
## 신뢰할 수 있고 사이트 구조가 변경되더라도 동작하는 스크래핑코드

- `페이지 인쇄` 링크를 찾아보거나, 더 나은 HTML 구조를 갖춘 모바일 버전 사이트를 찾아보자
- JS 파일에 숨겨진 정보를 찾아보자. 
  - ex) 사이트에 포함된 구글 맵스를 조작하는 자바스크립트를 살펴보고 위도와 경도가 포함된 거리 주소를 배열 형태로 수집하는 경우
- 중요 정보는 보통 페이지 타이틀에 있는 경우가 대부분이지만 원하는 정보가 페이지 URL에 들어있을 경우가 있다.
- 내가 원하는 정보가 이 웹사이트에만 존재하는가?
  - 이 정보를 다른 소스에서 가져올 수는 없을까?
  - 이 웹사이트의 정보가 다른 사이트의 정보는 아닐까?
  
---


## BeautifulSoup

### 1. findAll(tag, attributes, recursive, text, limit, keywords)
  - 이름과 속성에 따라 태그를 찾는 함수
  - `findAll`는 특정 태그에 들어있는 텍스트만 선택해서 고유명사로 이루어진 파이썬 리스트를 추출할 수 있다.
  - `recursive`: 기본적으로 재귀적으로 동작하며 자식 태그를 계속 탐색한다. `false`인 경우 최상위 태그만 찾는다.
  - `text`: 태그의 속성이 아니라 텍스트 콘텐츠에 일치한다.
  - `limit`: 페이지 항목 **처음 몇 개**에 관심있는 경우 설정한다. `find` 함수의 limit은 1이다.
  - `keyword`: 특정 속성이 포함된 태그를 선택할 때 사용한다.
  ```
  ex1) bs.findAll("span", {"class": "green"})
  ```
  ```
  ex2) bs.findAll({'h1', 'h2', 'h3', 'h4', 'h5', 'h6'})
  ```
  ```
  # 페이지에서 태그에 둘러싸인 the prince가 몇 번 나타났는지 확인 
  ex3) bs.findAll(text = 'the price')
  ```
  ```
  # 특정 속성이 포함된 태그를 선택하는 경우
  ex4) 
  bs.findAll(id='title')
  bs.findAll('', {'id' : 'title})
  ```

### 2. find
   
   - find(tag, attributes, recursive, text, keywords) 
  

---

### NavigableString 객체

- 태그 자체가 아니라 태그 안에 들어 있는 텍스트를 나타낸다.
- 일부 함수는 Navigable Strings를 다루거나 반환한다.

### Comment 객체
- 주석 태그 안에 들어있는 HTML 주석을 찾는데 용이하다.

---

## 트리 이동
- 문서 안에서 `위치`를 기준으로 태그를 찾을 경우
- https://www.pythonscraping.com/pages/page3.html 에서 크롤링 실습
<img src="./image/Screenshot%202022-02-21%20at%2023-22-07%20https%20www%20pythonscraping%20com.png" style="width:400px; margin-top:20px">

### 관계
- 자식: `children` - 자식만 찾을 경우 `.children()` 사용
- 자손: `descendants` - 자손을 찾을 경우 `.descendants()` 함수 사용

```
for child in bs.find("table", {"id": "giftList"}).children:
    print(child)
```

- 
```

```



