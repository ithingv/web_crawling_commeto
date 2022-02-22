from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("https://www.pythonscraping.com/pages/page1.html")
bs = BeautifulSoup(html, 'html.parser')

if __name__ == "__main__":
    print(bs.html.h1)
    print(bs.html.body.h1)
    print(bs.body.h1)
    