import time
import json
import logging
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import urljoin
import os.path
import sys
import time 

import utilities
from company import HomestarCompanyInfo

homestars_url = "https://www.homestars.com/"

def get_companies_urls(browser, max_scroll_downs):
    urls = []
    utilities.scroll_down(browser, ".next_page", 100)
    start = time.time()
    companies_results = browser.find_elements_by_css_selector("." + HomestarCompanyInfo.COMPANY_RESULTS_CSS_CLASS)
    for company_result in companies_results:
        ext_url = company_result.find_element_by_css_selector("." + HomestarCompanyInfo.COMPANY_URL_CSS_CLASS).find_element_by_tag_name("a").get_attribute("href")
        urls.append(ext_url)
    end = time.time()
    print("time = {}".format(end - start))
    print("extracted {} urls".format(len(urls)))
    urls = list(set(urls))
    print("Deleting overlaps, total left {} urls".format(len(urls)))
    browser.quit()

    return urls


def run_category_extraction(url, companies_infos, keyword):
    try:
        company = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
        company.extract_company()
        companies_infos.append(company.company_info)
    except:
        time.sleep(3)
        try :
            company = HomestarCompanyInfo(urljoin(homestars_url, url), keyword)
        except Exception as e:
            logging.error("url : {}.  {}".format(url, str(e)))


def extract_category(browser: webdriver, keyword, location, threads_num, max_scroll_downs):
    url_file_name = "{}_{}_urls.txt".format(location, keyword)
    print("Obtaining shops urls for \"{}\" keyword in \"{}\" location".format(keyword, location))
    if os.path.isfile(url_file_name):
        companies_urls = utilities.read_urls_from_file(url_file_name)
        print("Using already extracted urls from {} file".format(url_file_name))
    else:
        companies_urls = get_companies_urls(browser, max_scroll_downs)
        utilities.write_urls_to_file("{}_{}_urls.txt".format(location, keyword), companies_urls)

    # run_category_extraction(companies_urls[0], companies_infos, keyword)
    companies_infos = []
    trds = []
    print("Extracting data for \"{}\" keyword in \"{}\" location".format(keyword, location))
    i = 0
    total = len(companies_urls)
    for url in companies_urls:
        i += 1
        sys.stdout.write("\r[Extracting: {}/{}]".format(i, total))
        sys.stdout.flush()
        time.sleep(0.3)
        t = threading.Thread(target=run_category_extraction, args=(url, companies_infos, keyword))
        t.daemon = True
        t.start()
        trds.append(t)
        while threading.active_count() > threads_num:
            time.sleep(0.4)
    print("l2")
    for i in trds:
        i.join(10)
    print("l4")
    logging.info("Finished. keyword: {},  companies: {}".format(keyword, len(companies_infos)))
    return companies_infos
