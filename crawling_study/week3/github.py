from requests_html import HTMLSession
session = HTMLSession()

r = session.get('https://github.com/ithingv')

print(r.text)