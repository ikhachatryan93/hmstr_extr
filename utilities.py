from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time


def setup_phantomjs_browser(maximize=False):
    service_args = ['--ignore-ssl-errors=true', '--ssl-protocol=any']
    phantomjs = webdriver.PhantomJS("phantomjs.exe", service_args=service_args)
    if maximize:
        phantomjs.maximize_window()

    return phantomjs


def setup_chrome_browser(maximize=False):
    chrome = webdriver.Chrome("chromedriver.exe")  # , chrome_options=chrome_options)
    if maximize:
        chrome.maximize_window()
    return chrome


def write_urls_to_file(name, urls):
    with open(name, 'w', encoding='utf-8') as f:
        for url in urls:
            try:
                f.write(url + '\n')
            except Exception as e:
                print(str(e))


def scroll_down(driver: webdriver, css_selector: str):
    wait = WebDriverWait(driver, 10)
    while True:
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, css_selector)))
        driver.execute_script("window.scrollTo(0, 0)")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        click_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, css_selector)))
        if "disabled" in click_element.get_attribute("class"):
            break
        # print("asd")
        driver.save_screenshot("asd.png")


def open_url(url_query: str, driver: webdriver):
    driver.get(url_query)