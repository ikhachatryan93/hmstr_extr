import time
from bs4 import BeautifulSoup
from urllib.request import urljoin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import utilities
from company import HomestarCompanyInfo

next_page_css_selector = ".next_page"
homestars_url = "https://www.homestars.com/"

def get_companies_in_soup(browser: webdriver, scroll_down=True):
    if scroll_down:
        utilities.scroll_down(browser, next_page_css_selector)
    soup = BeautifulSoup(browser.page_source, "html5lib")
    return soup.findAll("section", {"class", HomestarCompanyInfo.COMPANY_RESULTS_CSS_CLASS})


def get_companies_in_browser(browser: webdriver, scroll_down=True):
    if scroll_down:
        utilities.scroll_down(browser, next_page_css_selector)
    return browser.find_elements_by_css_selector(('.' + HomestarCompanyInfo.COMPANY_RESULTS_CSS_CLASS))


def get_category(company):
    category_tags = company.find("div", {"class": HomestarCompanyInfo.COMPANY_CATEGORY_CSS_CLASS}).findAll("a")
    categories = ""
    for category_tag in category_tags:
        categories += category_tag.get_text() + ", "
    return categories.split(", ")


def extract_services(browser: webdriver):
    companies = get_companies_in_soup(browser)
    companies_info_list = []
    for company in companies:
        company_info = HomestarCompanyInfo()

        # get company url
        name = company.find("h1", {"class": HomestarCompanyInfo.COMPANY_URL_CSS_CLASS})
        company_info.add_info("url_name", urljoin(homestars_url, name.a["href"]))

        # get company name
        company_info.add_info("shop_name", name.a.get_text())

        # get category of the company
        categories = get_category(company)
        company_info.add_info("category_name", categories)

        companies_info_list.append(company_info)
