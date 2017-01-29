import time
from bs4 import BeautifulSoup
from urllib.request import urljoin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import utilities

homestars_url = "https://www.homestars.com/"


class HomestarCompanyInfo:
    COMPANY_RESULTS_CSS_CLASS = "company-result"
    COMPANY_URL_CSS_CLASS = "company-result__name"
    COMPANY_CATEGORY_CSS_CLASS = "company-result__categories"

    def __init__(self, company_url, browser_name="chrome"):
        self.company_info = dict(
            url_id="", url_name=company_url, category_id="", category_name="", keyword="",
            keyword_name="", shop_id="", shop_name="", shop_logo="", contact_person_name="",
            phone="", country_id="", country_name="", province="", city="", location="",
            address="", year_established="", no_of_employees="", payment_method="", licenses="",
            workers_compensation="", is_bounded="", warranty_terms="", written_contract="",
            project_rate="", project_minimum="", liability_insurance="", website="", homestars_star_score="",
            homestars_rating="", homestars_total_reviews="", homestars_review_id="", homestars_reviews=[],
            homestars_review_user_id="", homestars_review_user_name="", homestars_review_date="",
            homestars_review_location="", shop_photos="", shop_profile_id="", shop_profile_desc="")

        if "phantomjs" in browser_name:
            self.driver = utilities.setup_phantomjs_browser()
        else:
            self.driver = utilities.setup_chrome_browser()

        self.company_page = self.driver.get(self.company_info["url_name"])
        self.company_page_soup = BeautifulSoup(self.company_page.page_source, "html5lib")

    def get_categories(self):
        category_tag = self.company_page.find_element_by_xpath(".//*[@id='listing_content']/div[1]/a[2]")
        self.company_info["category_name"] = category_tag.text.split(" in ")[0].strip()

    def get_company_name(self):
        company_name = self.company_page.find_element_by_css_selector(".company-header__name>h1").text
        self.company_info["company_name"] = company_name.strip()

    #def get_owner(self):
    #    owner = self.company_page.find_element_by_css_selector(".company-header__name>h1").text
    #    self.company_info["company_name"] = company_name.strip()

    # def get_url_name(self):
    #    name = self.category_search_result.find("h1", {"class": HomestarCompanyInfo.COMPANY_URL_CSS_CLASS})
    #    return urljoin(homestars_url, name.a["href"])

    # def get_company_name(self):
    #    name = self.category_search_result.find("h1", {"class": HomestarCompanyInfo.COMPANY_URL_CSS_CLASS})
    #    return name.a.get_text

    # def extract_company_url(self):
    #    # get company url
    #    self.company_info["url_name"] = self.get_url_name()

    def extract_company(self):
        pass
        self.driver.quit()

    def __del__(self):
        pass

        ## get company name
        # self.company_info["shop_name"] = self.get_company_name()

        ## get category of the company
        # self.company_info["category_name"] = self.get_categories()
