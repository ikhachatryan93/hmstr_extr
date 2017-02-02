import time
import logging
import threading
from datetime import datetime
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urljoin

import utilities
from company import HomestarCompanyInfo

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

log_name = datetime.now().strftime('search_%H_%M_%d_%m_%Y.log')
fileHandler = logging.FileHandler(filename=log_name)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)

# consoleHandler = logging.StreamHandler()
# consoleHandler.setFormatter(logFormatter)
# rootLogger.addHandler(consoleHandler)
logging.basicConfig(level=logging.ERROR)

homestars_url = "https://www.homestars.com/"


def get_companies_urls(browser, max_scroll_downs):
    try:
        utilities.scroll_down(browser, ".next_page", max_scroll_downs)
    except Exception as e:
        logging.ERROR("Could not get urls for: {}".format(str(e)))
        return []
    soup = BeautifulSoup(browser.page_source, "html5lib")
    browser.close()
    companies_results = soup.findAll("section", {"class", HomestarCompanyInfo.COMPANY_RESULTS_CSS_CLASS})
    urls = []
    for company_result in companies_results:
        urls.append(company_result.find("h1", {"class": HomestarCompanyInfo.COMPANY_URL_CSS_CLASS}).a["href"])

    return urls


def run_category_extraction(url, companies_infos, keyword):
    try:
        company_info = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
        c = company_info.extract_company()
        companies_infos.append(c)
    except Exception as e:
        logging.error("url : {}.  {}".format(url, str(e)))


def extract_category(browser: webdriver, keyword, threads_num, max_scroll_downs):
    logging.debug("Extracting {} keyword".format(keyword))
    companies_urls = get_companies_urls(browser, max_scroll_downs)
    companies_infos = []
    #run_category_extraction(companies_urls[0], companies_infos, keyword)
    trds = []
    for url in companies_urls:
        t = threading.Thread(target=run_category_extraction, args=(url, companies_infos, keyword))
        t.daemon = True
        t.start()
        trds.append(t)
        while threading.active_count() > threads_num:
            time.sleep(0.2)

    for i in trds:
       i.join(60*60)

    logging.debug("Finished. keyword: {},  companies: {}".format(keyword, len(companies_urls)))

    return companies_infos
