from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import json
import random


def setup_phantomjs_browser(maximize=False):
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
    phantomjs = webdriver.PhantomJS("phantomjs.exe", service_args=service_args)
    if maximize:
        phantomjs.maximize_window()

    return phantomjs


def setup_chrome_browser(maximize=True):
    chrome = webdriver.Chrome("chromedriver")
    if maximize:
        chrome.maximize_window()
    return chrome


#def setup_chrome_browser(maximize=True):
#    with open('proxies.txt') as f:
#        lines = f.readlines()
#        PROXY = random.choice(lines)
#    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--proxy-server=%s' % PROXY)
#    chrome = webdriver.Chrome("chromedriver", chrome_options=chrome_options)
#    if maximize:
#        chrome.maximize_window()
#    return chrome

def read_urls_from_file(name):
    urls = []
    with open(name, encoding='utf-8') as f:
        urls = f.read().splitlines() 
    assert(len(urls) > 0)
    return urls

def write_urls_to_file(name, urls):
    with open(name, 'w', encoding='utf-8') as f:
        for url in urls:
            try:
                f.write(url + '\n')
            except Exception as e:
                print(str(e))

def write_json_file(name, data):
    with open(name, 'w') as fname:
        json.dump(data, fname)


# return false if scrolldowns ended
def scroll_down(driver, css_selector, max_scroll_downs):
    wait = WebDriverWait(driver, 10)
    for _ in range(max_scroll_downs):
        try:
            wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException:
            return False
        except OSError:
            print("scroll down error")
            time.sleep(2)
            continue
        driver.execute_script("window.scrollTo(0, 0)")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            click_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        except TimeoutException:
            return False
        try:
            if "disabled" in click_element.get_attribute("class"):
                return False
        except:
            continue

    return True


def open_url(url_query: str, driver: webdriver):
    driver.get(url_query)
