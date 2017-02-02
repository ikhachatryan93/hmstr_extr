#! /bin/env python
import utilities
import homestars
import configparser
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

homestars_url = "https://www.homestars.com/"

search_locations_list = ""
search_keywords_list = ""

search_by_category_name_match = False
search_by_company_name_match = False

threads = 1
max_category_scroll_downs = 1000


def parse_config_file():
    config_parser = configparser.RawConfigParser()
    config_file = r'./configs.txt'
    config_parser.read(config_file)

    global search_locations_list
    global search_keywords_list
    global search_by_category_name_match
    global search_by_company_name_match
    global max_category_scroll_downs
    global threads

    search_keywords_list = config_parser.get('search_info', 'keywords')
    search_locations_list = config_parser.get('search_info', 'locations')

    search_by_category_name_match = config_parser.getboolean('search_info', 'category_name_match')
    search_by_company_name_match = config_parser.getboolean('search_info', 'company_name_match')
    max_category_scroll_downs = config_parser.getint('search_info', 'max_category_scroll_downs')

    threads = config_parser.getint('parameters', 'threads')


def search_keyword_in_location(keyword, location, browser, search_type="category_name"):
    utilities.open_url(homestars_url, browser)

    # input keyword
    keyword_input = browser.find_element_by_css_selector("#hero_keyword_search")
    keyword_input.clear()
    keyword_input.send_keys(keyword)

    # input location
    location_input = browser.find_element_by_css_selector("#hero_location_search")
    location_input.clear()
    location_input.send_keys(location)

    # needed to get correct search results
    time.sleep(3)

    # search
    search_button = browser.find_element_by_css_selector(".hero-search__button")
    search_button.click()

    wait = WebDriverWait(browser, 15)
    if "company_name" in search_type:
        try:
            company_name_match_button = wait.until(
                EC.presence_of_element_located((By.XPATH, "html/body/div[5]/div[1]/div[2]/div/div/div/div[2]/div/a")))
        except TimeoutException:
            return
        company_name_match_button.click()

    browser.save_screenshot("start.png")


def extract(location, keyword, search_type="company_name"):
    # browser= utilities.setup_phantomjs_browser(maximize=True)
    browser = utilities.setup_chrome_browser(maximize=True)
    search_keyword_in_location(keyword, location, browser, search_type)
    extracted_services = homestars.extract_category(browser, keyword, threads, max_category_scroll_downs)

    # utilities.save_as_jquery(extracted_services)


def main():
    parse_config_file()
    for keyword in search_keywords_list.split(","):

        # search results for company name mach have not location,
        # the results are for all country
        # so we can just search the keyword without location
        if search_by_company_name_match:
            extract("", keyword, "company_name")

        # for search by category action a location is required.
        if search_by_category_name_match:
            for location in search_locations_list.split(","):
                extract(location, keyword, "category_name")


if __name__ == "__main__":
    main()
