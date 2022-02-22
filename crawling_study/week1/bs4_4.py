from urllib.request import urlopen
from bs4 import BeautifulSoup


if __name__ == "__main__":
    url = "https://www.pythonscraping.com/pages/warandpeace.html"
    html = urlopen(url)
    bs = BeautifulSoup(html, "html.parser")
    contents = bs.findAll("span", {"class": "green"})

    for content in contents:
        print(content.get_text())
