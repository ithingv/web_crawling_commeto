from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time


# 페이지 맨 아래로 이동

articles_list = []

for i in range(10850):

    url = "https://seekingalpha.com/earnings/earnings-call-transcripts?page={}".format(i+1)
    driver.get(url)
    time.sleep(3)
    
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    
    articles = soup.find_all("article", {"class" : "ukA vaA yA bbW bbBH xjA bbL bbCA xjA bbL bbCA xjE xjE ukB"})
    for article in articles:  
        try:            
            articles_list.append(
                    {
                        "title" : article.select("a")[0].get("aria-label").strip(),
                        "link"  : urljoin("https://seekingalpha.com/", article.select("a")[1].get("href")),
                        "ticker" : [ticker.text.strip() for ticker in article.find_all("a", {"data-test-id" : "post-list-ticker"})],
                        "author" : article.find("a", {"data-test-id" : "post-list-author"}).text.strip(),
                        "date" : date_converter(article.find("span", {"data-test-id": "post-list-date"}).text.strip())
                    }
            )

        except:
            print(f"Error Occur in {i+1} page")
            continue
        
        print(f"{i + 1} page done")
    
print(articles_list)
