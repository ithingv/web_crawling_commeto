from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://www.opencart.com/")

    # login form
    page.fill('input#login-id', 'your id')
    page.fill('input#login-password', 'your password')
    
    # click login button 
    page.click('button[type=submit]')

    # page.is_visible('div.tile-body')
    # select content 
    html = page.inner_html('#content')
    soup = BeautifulSoup(html, 'html.parser')
