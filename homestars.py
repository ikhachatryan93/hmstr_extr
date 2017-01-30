import time
from bs4 import BeautifulSoup
from urllib.request import urljoin
from selenium import webdriver
from queue import Queue
import threading
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import utilities
from company import HomestarCompanyInfo

next_page_css_selector = ".next_page"
homestars_url = "https://www.homestars.com/"


def get_companies_urls(browser: webdriver, scroll_down=True):
    if scroll_down:
        utilities.scroll_down(browser, next_page_css_selector, 1)
    soup = BeautifulSoup(browser.page_source, "html5lib")
    browser.close()
    companies_results = soup.findAll("section", {"class", HomestarCompanyInfo.COMPANY_RESULTS_CSS_CLASS})
    urls = []
    for company_result in companies_results:
        urls.append(company_result.find("h1", {"class": HomestarCompanyInfo.COMPANY_URL_CSS_CLASS}).a["href"])

    return urls


def run_category_extraction(url, companies_infos):
    company_info = HomestarCompanyInfo(urljoin(homestars_url, url))
    c = company_info.extract_company()
    companies_infos.append(c)


def extract_category(browser: webdriver, parallel=1):
    companies_urls = get_companies_urls(browser)
    companies_infos = []
    run_category_extraction(companies_urls[0], companies_infos)
   # trds = []
   # for url in companies_urls:
   #     t = threading.Thread(target=run_category_extraction, args=(url, companies_infos))
   #     t.daemon = True
   #     t.start()
   #     trds.append(t)
   #     while threading.active_count() > parallel:
   #         time.sleep(0.2)

   # for i in trds:
   #     i.join()

    return companies_infos
