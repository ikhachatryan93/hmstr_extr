import time
from bs4 import BeautifulSoup
from urllib.request import urljoin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import utilities
import logging

homestars_url = "https://www.homestars.com/"


class HomestarCompanyInfo:
    COMPANY_RESULTS_CSS_CLASS = "company-result"
    COMPANY_URL_CSS_CLASS = "company-result__name"
    COMPANY_CATEGORY_CSS_CLASS = "company-result__categories"
    NF = "Could not find "
    logging.basicConfig(filename='scraping.log', level=logging.DEBUG)

    def __init__(self, company_url, browser_name="chrome"):
        self.company_info = dict(
            url_id="", url_name=company_url, category_id="", category_name="", keyword="",
            keyword_name="", shop_id="", shop_name="", shop_logo="", contact_person_name="",
            phone="", country_id="", country_name="", province="", city="", location="",
            address="", year_established="", number_of_employees="", payment_methods="", licenses="",
            workers_compensation="", is_bonded="", warranty_terms="", written_contract="",
            project_rate="", project_minimum="", liability_insurance="", website="", homestars_star_score="",
            homestars_rating="", homestars_total_reviews="", homestars_review_id="", homestars_reviews=[],
            homestars_review_user_id="", homestars_review_user_name="", homestars_review_date="",
            homestars_review_location="", shop_photos="", shop_profile_id="", shop_profile_desc="")

        if "phantomjs" in browser_name:
            self.company_page = utilities.setup_phantomjs_browser()
        else:
            self.company_page = utilities.setup_chrome_browser()

        self.company_page.get(self.company_info["url_name"])
        self.company_page_source = BeautifulSoup(self.company_page.page_source, "html5lib")
        self.company_profile_details = self.company_page_source.find("div", {"class", "company-profile__details"})
        self.company_address_info = self.company_page_source.find("address", {"class": "company-header__address"})

    def get_categories(self):
        try:
            categories = self.company_profile_details.find("dt", text="CATEGORIES").find_next_sibling("dd").get_text()
        except:
            try:
                category_tag = self.company_page.find_element_by_xpath(".//*[@id='listing_content']/div[1]/a[2]")
                categories = category_tag.text.split(" in ")[0].strip()
            except NoSuchElementException:
                logging.error(self.NF + "category names")
                return

        self.company_info["category_name"] = categories.split(", ")

    def get_company_name(self):
        try:
            company_name = self.company_page.find_element_by_css_selector(".company-header__name>h1").text
        except NoSuchElementException:
            logging.error(self.NF + "company name")
            return

        self.company_info["company_name"] = company_name.strip()

    def get_contact_person_name(self):
        try:
            contact_person = self.company_page.find_element_by_css_selector(".owner__name").text
        except NoSuchElementException:
            logging.warning(self.NF + "contact person name")
            return

        self.company_info["contact_person_name"] = contact_person.split("[")[0].strip()

    def get_region(self):
        province = self.company_address_info.find("span", {"itemprop": "addressRegion"})
        if province is None:
            logging.error(self.NF + "region")
            return

        self.company_info["province"] = province.get_text().strip(", ")

    def get_city(self):
        try:
            city = self.company_page.find_element_by_css_selector(".city-name").text
        except NoSuchElementException:
            logging.error(self.NF + "city")
            return

        self.company_info["city"] = city.strip()

    def get_address(self):
        address = self.company_address_info.find("spam", {"itemprop": "streetAddress"})
        if address is None:
            logging.error(self.NF)
            return

        self.company_info["address"] = address.get_text().strip(", ")

    def get_postal(self):
        postal = self.company_address_info.find("span", {"itemprop": "postalCode"})
        if postal is None:
            logging.error(self.NF + "postal code")
            return

        self.company_info["postal_code"] = postal.get_text().strip(", ")

    def get_description(self):
        try:
            desk = self.company_page.find_element_by_css_selector(".company-profile__description").text
        except NoSuchElementException:
            logging.warning(self.NF + "description")
            return
        self.company_info["shop_profile_desc"] = desk.strip()

    def get_waranty_terms(self):
        try:
            warranty_terms = self.company_profile_details.find("dt", text="WARRANTY TERMS").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "warranty terms")
            return

        self.company_info["warranty_terms"] = warranty_terms.split(", ")

    def get_bonded(self):
        try:
            bonded = self.company_profile_details.find("dt", text="BONDED").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "bonded")
            return

        self.company_info["is_bonded"] = bonded.split(", ")

    def get_project_rate(self):
        try:
            rate = self.company_profile_details.find("dt", text="PROJECT RATE").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "project rate")
            return

        self.company_info["project_rate"] = rate.split(", ")

    def get_project_minimum(self):
        try:
            name = self.company_profile_details.find("dt", text="PROJECT MINIMUM").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "project minimum")
            return

        self.company_info["project_minimum"] = name.split(", ")

    def get_liability_insurance(self):
        try:
            liab_insurance = self.company_profile_details.find("dt", text="LIABILITY INSURANCE").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "liability insurance")
            return
        self.company_info["liability_insurance"] = liab_insurance.split(", ")

    def get_number_of_employees(self):
        try:
            num_of_employees = self.company_profile_details.find("dt", text="NUMBER OF EMPLOYEES").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "number of employees")
            return

        self.company_info["number_of_employees"] = num_of_employees.split(", ")

    def get_payment_methods(self):
        try:
            payment_methods = self.company_profile_details.find("dt", text="PAYMENT METHOD").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "payment methods")
            return

        self.company_info["payment_methods"] = payment_methods.split(", ")

    def get_year_established(self):
        try:
            year_established = self.company_profile_details.find("dt", text="YEAR ESTABLISHED").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "year established")
            return

        self.company_info["year_established"] = year_established.split(", ")

    def get_written_contract(self):
        try:
            writtent_contract = self.company_profile_details.find("dt", text="WRITTEN CONTRACT").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "written contract")
            return

        self.company_info["written_contract"] = writtent_contract.split(", ")

    def get_website_url(self):
        try:
            website_url = self.company_profile_details.find("dt", text="WEBSITE").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "website url")
            return

        self.company_info["website"] = website_url.split(", ")

    def get_workers_compensation(self):
        try:
            comp = self.company_profile_details.find("dt", text="WORKERS COMPENSATION").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "website url")
            return

        self.company_info["workers_compensation"] = comp.split(", ")

    def get_licences(self):
        try:
            licenses = self.company_profile_details.find("dt", text="LICENSES").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "licenses")
            return

        self.company_info["licenses"] = licenses.split(", ")

    def get_phone(self):
        #try:
        phone_button = self.company_page.find_element_by_css_selector(".company-contact-buttons__button--phone")
        phone_button.click()
        phone_button = self.company_page.find_element_by_css_selector(".company-contact-buttons__button--phone")
        phone = phone_button.text
        #except:
        #    logging.warning(self.NF + "phone number")
        #    return

        self.company_info["phone"] = phone.split(", ")

    def extract_company(self):
        self.get_phone()
        pass
        self.company_page.quit()

    def __del__(self):
        pass

        ## get company name
        # self.company_info["shop_name"] = self.get_company_name()

        ## get category of the company
        # self.company_info["category_name"] = self.get_categories()
