from urllib.request import urlopen

html = urlopen("https://www.pythonscraping.com/pages/page1.html")

if __name__ == "__main__":
    print(html.read())