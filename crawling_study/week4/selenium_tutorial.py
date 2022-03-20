# Driver install

# Chrome	https://sites.google.com/a/chromium.org/chromedriver/downloads
# Edge	https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/
# Firefox	https://github.com/mozilla/geckodriver/releases
# Safari	https://webkit.org/blog/6900/webdriver-support-in-safari-10/


from selenium import webdriver

# 윈도우 사이즈
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920, 1000')

# Headless

options.add_argument('headless')

driver = webdriver.Chrome('chromedriver.exe', options=options)

# Max window
# options.add_argument('start-maximized')
driver.maximize_window()

driver.close() # 현재 탭 닫기
driver.quit() # 브라우저 닫기

driver.back() # 뒤로가기
driver.forward() # 앞으로가기

# 브라우저 탭 객체 리스트
driver.window_handles

# 첫번째 탭으로 이동
driver.switch_to_window(driver.window_handles[0])
# 두번째 탭으로 이동
driver.switch_to_window(driver.window_handles[1])

# 탭 닫기
driver.switch_to.window(driver.window_handles[0]) #닫을 탭으로 이동 후
driver.close()

# 엘리먼트 접근
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/button/span[2]') #xpath 로 접근
driver.find_element_by_class_name('ico_search_submit')  #class 속성으로 접근
driver.find_element_by_id('ke_kbd_btn') #id 속성으로 접근
driver.find_element_by_link_text('회원가입')    #링크가 달려 있는 텍스트로 접근
driver.find_element_by_css_selector('#account > div > a')   #css 셀렉터로 접근
driver.find_element_by_name('join') #name 속성으로 접근
driver.find_element_by_partial_link_text('가입')  #링크가 달려 있는 엘레먼트에 텍스트 일부만 적어서 해당 엘레먼트에 접근
driver.find_element_by_tag_name('input')    #태그 이름으로 접근

driver.find_element_by_tag_name('input').find_element_by_tag_name('a')  #input 태그 하위태그인 a 태그에 접근
driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div/div[3]/form/fieldset/button/span[2]').find_element_by_name('join') #xpath 로 접근한 엘레먼트의 안에 join 이라는 속성을 가진 tag 엘레먼트에 접근

# 엘리먼트 클릭
driver.find_element_by_id('ke_kbd_btn').click()

# 텍스트 입력
driver.find_element_by_id('ke_awd2_btn').send_keys('텍스트 입력')

# 텍스트 삭제
driver.find_element_by_id('ke_awd2_btn').clear()

# 단축키 입력
from selenium.webdriver.common.keys import Keys

# ctrl+v
driver.find_element_by_id('ke_kbd_btn').send_keys(Keys.CONTROL + 'v')

# 다른 방법
from selenium.webdriver import ActionChains

ActionChains(driver).key_down(Keys.CONTROL).send_keys('V').key_up(Keys.CONTROL).perform() 
#위에서 driver 대신 엘리먼트를 입력해도 좋음. 

# Frame 이동

# 이동할 프레임 엘리먼트 지정
element = driver.find_element_by_tag_name('iframe')

# Frame 이동
driver.switch_to_frame(element)

# 프레임에서 빠져나오기
driver.switch_to_default_content()

# 경고창
driver.switch_to_alert

# 경고창 수락/거절
from selenium.webdriver.common.alert import Alert

Alert(driver).accept() # 경고창 수락 누름
Alert(driver).dismiss() # 경고창 거절 누름
print(Alert(driver).text) # 경고창 텍스트 얻음


# Cookie
# 쿠키 얻기
driver.get_cookies()

# 쿠키 추가
driver.add_cookie()

# 모든 쿠키 삭제
driver.delete_all_cookies()

# 특정 쿠키 삭제
driver.delete_cokkie(cookie_name)

# Javascript 코드 실행

# 브라우저 스크롤 최하단으로 이동
driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

# CSS 셀렉터로 클릭
driver.execute_script("document.querySelector('body > div.modal-options__buttons > button.btn.btn-primary').click();")

# OR
# elemToclick = driver.~~~
# driver.execute_script('arguments[0].click();', elemToclick)
# driver.find_element_by_css_selector(~~).click() 과 동일하나 이 코드가 작동하지 않을시 자바스크립트 코드를 시도해볼만하다.

# 스크롤 특정 엘리먼트로 이동
element = driver.find_element_by_css_selector('div > a')
driver.execute_script('arguments[0].scrollIntoView(true);', element)

# 스크린샷
# 캡처할 엘리먼트 지정

element = driver.driver.find_element_by_class_name('ico.search_submit')
# capture
element.save_screenshot('image.png')

# ERROR HANDLING
from selenium.common.exceptions import NoAlertPresentException, NoSuchElementException, TimeoutException, ElementNotInteractableException,NoSuchWindowException, NoSuchFrameException

# NoAlertPresentException 경고창 관련 명령어를 실행했으나 현재 경고창이 뜨지 않음
# NoSuchElementException 엘레먼트 접근하였으나 없음
# TimeoutException 특정한 액션을 실행하였으나 시간이 오래 지나도록 소식이 없음
# ElementNotInteractableException 엘리먼트에 클릭등을 하였으나 클릭할 성질의 엘리먼트가 아님
# NoSuchWindowException 해당 윈도우 없음
# NoSuchFrameException 해당 프레임 없음


# Shadow dom 처리
#shadow dom 엘레먼트 열어주는법
element = driver.execute_script("return document.querySelector('#syndi_powerpage > div').shadowRoot").get_attribute('innerHTML') # css Selector 이용 # element 의 HTML 내용 return
# shadow dom 처리를 통한 크롬 인터넷 기록 삭제

def expand_shadow_element(element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

driver.get('chrome://settings/clearBrowserData')

elem = driver.find_element_by_css_selector('body > settings-ui')
elem1 = expand_shadow_element(elem)
elem1 = elem1.find_element_by_id('main')
elem2 = expand_shadow_element(elem1)
elem2 = elem2.find_element_by_tag_name('settings-basic-page')
elem3 = expand_shadow_element(elem2)
elem3 = elem3.find_element_by_tag_name('settings-privacy-page')
elem4 = expand_shadow_element(elem3)
elem4 = elem4.find_element_by_tag_name('settings-clear-browsing-data-dialog')
elem5 = expand_shadow_element(elem4)
elem5forconfirmelem = expand_shadow_element(elem4) # 인터넷 사용기록 삭제버튼 클릭을 위한 엘레먼트 따로 빼놓기
elem5 = elem5.find_element_by_id('clearFromBasic')
elem6 = expand_shadow_element(elem5)
elem6 = elem6.find_element_by_id('dropdownMenu')
elem6.find_element_by_css_selector('option[value="4"]').click() # 전체기간 선택
elem5forconfirmelem.find_element_by_id('clearBrowsingDataConfirm').click() # 인터넷 사용기록 삭제버튼 클릭

# xhr data
from selenium.webdriver import DesiredCapabilities
import json

capabilities = DesiredCapabilities.CHROME
capabilities["goog:loggingPrefs"] = {"performance": "ALL"}  # newer: goog:loggingPrefs

try:
    s = Service(f'./{chrome_ver}/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=option, desired_capabilities=capabilities)
except:
    chromedriver_autoinstaller.install(True)
    s = Service(f'./{chrome_ver}/chromedriver.exe')
    driver = webdriver.Chrome(service=s, options=option, desired_capabilities=capabilities)
driver.implicitly_wait(7)

driver.get('blablablabla~~~')

logs_raw = driver.get_log("performance")
logs = [json.loads(lr["message"])["message"] for lr in logs_raw]

def log_filter(log_):
    return (
        # is an actual response
        log_["method"] == "Network.responseReceived"
        # and json
        and "json" in log_["params"]["response"]["mimeType"]
    )

for log in filter(log_filter, logs):
    request_id = log["params"]["requestId"]
    resp_url = log["params"]["response"]["url"]
    print(f"Caught {resp_url}")
    print(driver.execute_cdp_cmd("Network.getResponseBody", {"requestId": request_id}))

