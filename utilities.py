from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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


def scroll_down(driver: webdriver, css_selector: str, max_scrolls=10000000):
    wait = WebDriverWait(driver, 10)
    last_size = 0
    for _ in range(max_scrolls):
        current_size = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var "
                                             "lenOfPage=document.body.scrollHeight;return lenOfPage;")
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
            if last_size == current_size:
                if "disabled" not in driver.find_element_by_css_selector(css_selector).get_attribute("class"):
                    current_size = driver.execute_script("window.scrollTo(0, 0);var "
                                                         "lenOfPage=document.body.scrollHeight;return lenOfPage;")
                    continue
                break
        except TimeoutException:
            break
        except:
            pass
        last_size = current_size


def open_url(url_query: str, driver: webdriver):
    driver.get(url_query)
