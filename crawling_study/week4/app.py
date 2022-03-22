from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

s = Service(ChromeDriverManager().install())
o = webdriver.ChromeOptions()
# o.add_argument('headless')

driver = webdriver.Chrome(service=s, options=o)
driver.get("https://seekingalpha.com/symbol/FB/earnings/transcripts")
driver.maximize_window()
time.sleep(5)

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

with open("result.txt", "w", encoding='utf-8') as f:
    print(soup)
    f.write(str(soup))