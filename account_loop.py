from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from fake_useragent import UserAgent
# import accountInfoGenerator as account
# import getVerifCode as verifiCode
# import fakeMail as email
import random
import json

def login_loop(browser, username, passwd):
    browser.get("https://www.instagram.com/")
    time.sleep(1)

    #Fill the email value
    WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='react-root']/section/main/article/div/div/div/div[2]/button")
        )
    ).click()

    ### Login page
    WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='loginForm']/div[1]/div[1]/button")
        )
    )

    element_present = EC.presence_of_element_located(
        (By.NAME, 'username')
    )
    username_field = WebDriverWait(browser, 30).until(element_present)
    username_field.send_keys(username)
    time.sleep(0.5)

    fullname_field = browser.find_element_by_name('password')
    fullname_field.send_keys(passwd)
    # print(passwd)
    time.sleep(0.5)

    WebDriverWait(browser, 30).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//*[@id='loginForm']/div[1]/div[6]/button")
        )
    ).click()
    time.sleep(0.5)

    ### Pass save account
    for i in range(30):
        try:
            browser.find_element_by_xpath(    
                "//*[@id='react-root']/section/main/div/div/div/button"
            ).click()
            time.sleep(1)
        except:
            pass
        try:
            browser.find_element_by_xpath(    
                "/html/body/div[4]/div/div/div/div[3]/button[2]"
            ).click()
        except:
            pass
        try:
            WebDriverWait(browser, 0.5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//*[@id='react-root']/section/nav[2]/div/div/div[2]/div/div/div[5]/a")
                )
            ).click()
            break
        except:
            pass
    if i >= 29:
        assert False

    ### is working done loop
    while True:
        pressed_key = input('Next user: press \'n\', Previous user: press \'p\': ')
        pressed_key = pressed_key.lower()
        if pressed_key == 'n':
            break
        elif pressed_key == 'p':
            break
        else:
            print('{} is unknown keyword'.format(pressed_key))

    return pressed_key


if __name__ == '__main__':
    result_jsonname = 'private/id_list.json'
    with open(result_jsonname, 'r') as f:
        text = f.read()
    id_list = json.loads(text)

    # proxy = 'IP:PORT'
    proxy = None

    id_i = 0
    while True:
        if id_i >= len(id_list):
            break
        try:
            username = id_list[id_i][0]
            passwd = id_list[id_i][1]
            
            if proxy is not None:
                webdriver.DesiredCapabilities.CHROME['proxy'] = {
                    "httpProxy": proxy,
                    "ftpProxy": proxy,
                    "sslProxy": proxy,
                    "noProxy": None,
                    "proxyType": "MANUAL",
                    "class": "org.openqa.selenium.Proxy",
                    "autodetect": False
                }
                webdriver.DesiredCapabilities.CHROME['acceptSslCerts'] = True

            options = webdriver.ChromeOptions()
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)

            # ua = UserAgent()
            # userAgent = ua.random
            # print(userAgent)
            # options.add_argument(f'user-agent={userAgent}') 

            options = webdriver.ChromeOptions()
            options.add_argument('--user-agent="Mozilla/5.0 (Linux; Android 9; SM-A102U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 Instagram 155.0.0.37.107 Android (28/9; 320dpi; 720x1468; samsung; SM-A102U; a10e; exynos7885; en_US; 239490550)"')

            browser = webdriver.Chrome("chromedriver_win32/chromedriver.exe", options=options)
            
            print('{}/{}, Current user: {}'.format(id_i+1, len(id_list), username))
            pressed_key = login_loop(browser, username, passwd)
            browser.quit()

            if pressed_key == 'p': 
                id_i -= 2 
                if id_i == -2:
                    print('{} is first user'.format(username))
                    id_i = -1 
            elif pressed_key == 'n':
                if (len(id_list)-1) == id_i:
                    print('{} is last user'.format(username))
            
            id_i += 1
        except Exception as e:
            id_i += 1
            print('Error from user: {}, please check later'.format(username))
            browser.quit()
            print(e)
        finally:
            # browser.quit()
            print()
            time.sleep(1)
