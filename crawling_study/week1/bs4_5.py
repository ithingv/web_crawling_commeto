from urllib.request import urlopen
from bs4 import BeautifulSoup

if __name__ == "__main__":
    url = "https://www.pythonscraping.com/pages/page3.html"
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    # print(bs.html)
    for child in bs.find("table", {"id": "giftList"}).children:
        print(child)
