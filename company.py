import time
import contextlib
from bs4 import BeautifulSoup
from urllib.request import urlopen
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
    logging.basicConfig(filename='scraping.log', level=logging.DEBUG)

    def __init__(self, company_url, browser_name="chrome"):
        self.company_info = dict(
            url_name=company_url, category_name="", keyword="",
            keyword_name="", shop_name="", shop_logo="", contact_person_name="",
            phone="", country_name="", province="", city="", location="",
            address="", year_established="", number_of_employees="", payment_methods="", licenses="",
            workers_compensation="", is_bonded="", warranty_terms="", written_contract="",
            project_rate="", project_minimum="", liability_insurance="", website="", homestars_star_score="",
            homestars_rating="", homestars_total_reviews="", homestars_reviews=[],
            homestars_review_user_name="", homestars_review_date="",
            homestars_review_location="", shop_photos_links=[], shop_profile_desc="")

        if "phantomjs" in browser_name:
            self.company_page = utilities.setup_phantomjs_browser()
        else:
            self.company_page = utilities.setup_chrome_browser()

        self.company_page.get(self.company_info["url_name"])
        self.company_page_source = BeautifulSoup(self.company_page.page_source, "html5lib")
        self.company_profile_details = self.company_page_source.find("div", {"class", "company-profile__details"})
        self.company_address_info = self.company_page_source.find("address", {"class": "company-header__address"})
        self.NF = "From {}: could not find ".format(self.company_info["url_name"])

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

        self.company_info["category_name"] = categories.strip(", ")

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

        self.company_info["warranty_terms"] = warranty_terms.strip(", ")

    def get_bonded(self):
        try:
            bonded = self.company_profile_details.find("dt", text="BONDED").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "bonded")
            return

        self.company_info["is_bonded"] = bonded.strip(", ")

    def get_project_rate(self):
        try:
            rate = self.company_profile_details.find("dt", text="PROJECT RATE").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "project rate")
            return

        self.company_info["project_rate"] = rate.strip(", ")

    def get_project_minimum(self):
        try:
            name = self.company_profile_details.find("dt", text="PROJECT MINIMUM").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "project minimum")
            return

        self.company_info["project_minimum"] = name.strip(", ")

    def get_liability_insurance(self):
        try:
            liab_insurance = self.company_profile_details.find("dt", text="LIABILITY INSURANCE").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "liability insurance")
            return
        self.company_info["liability_insurance"] = liab_insurance.strip(", ")

    def get_number_of_employees(self):
        try:
            num_of_employees = self.company_profile_details.find("dt", text="NUMBER OF EMPLOYEES").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "number of employees")
            return

        self.company_info["number_of_employees"] = num_of_employees.strip(", ")

    def get_payment_methods(self):
        try:
            payment_methods = self.company_profile_details.find("dt", text="PAYMENT METHOD").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "payment methods")
            return

        self.company_info["payment_methods"] = payment_methods.strip(", ")

    def get_year_established(self):
        try:
            year_established = self.company_profile_details.find("dt", text="YEAR ESTABLISHED").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "year established")
            return

        self.company_info["year_established"] = year_established.strip(", ")

    def get_written_contract(self):
        try:
            writtent_contract = self.company_profile_details.find("dt", text="WRITTEN CONTRACT").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "written contract")
            return

        self.company_info["written_contract"] = writtent_contract.strip(", ")

    def get_website_url(self):
        try:
            website_url = self.company_profile_details.find("dt", text="WEBSITE").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "website url")
            return

        self.company_info["website"] = website_url.strip(", ")

    def get_workers_compensation(self):
        try:
            comp = self.company_profile_details.find("dt", text="WORKERS COMPENSATION").find_next_sibling(
                "dd").get_text()
        except:
            logging.warning(self.NF + "website url")
            return

        self.company_info["workers_compensation"] = comp.strip(", ")

    def get_licences(self):
        try:
            licenses = self.company_profile_details.find("dt", text="LICENSES").find_next_sibling("dd").get_text()
        except:
            logging.warning(self.NF + "licenses")
            return

        self.company_info["licenses"] = licenses.strip(", ")

    def get_rating(self):
        try:
            rating = self.company_page.find_element_by_css_selector(".review-aggregate-rating__rating").text
        except:
            logging.warning(self.NF + "rating")
            return

        self.company_info["homestars_rating"] = rating.strip(", ")

    def get_phone(self):
        try:
            phone_button = self.company_page.find_element_by_css_selector(".company-contact-buttons__button--phone")
            phone_button.click()
            phone_button = self.company_page.find_element_by_css_selector(".company-contact-buttons__phone-number")
            phone = phone_button.text
        except:
            logging.warning(self.NF + "phone number")
            return

        self.company_info["phone"] = phone.strip(", ")

    def get_location(self):
        try:
            location = self.company_page.find_element_by_css_selector(".service-area__map").get_attribute("src")
        except:
            logging.warning(self.NF + "location")
            return

        self.company_info["location"] = location.strip(", ")

    def get_all_images(self):
        try:
            see_more = self.company_page.find_element_by_css_selector(".square-gallery__see-more").click()
            photos_tags = self.company_page.find_elements_by_css_selector(".square-gallery__link")
            for p in photos_tags:
                self.company_info['shop_photos_links'].append(p.get_attribute("href"))
            # go back to company main page
            self.company_page.execute_script("window.history.go(-1)")
        except:
            try:
                photos_tags = self.company_page.find_elements_by_css_selector(".square-gallery__link")
                for p in photos_tags:
                    self.company_info['shop_photos_links'].append(p.get_attribute("href"))
            except:
                logging.warning(self.NF + "photos")

    def extract_company(self):
        self.get_address()
        self.get_phone()
        self.get_region()
        self.get_categories()
        self.get_contact_person_name()
        self.get_postal()
        self.get_bonded()
        self.get_city()
        self.get_company_name()
        self.get_description()
        self.get_liability_insurance()
        self.get_licences()
        self.get_number_of_employees()
        self.get_waranty_terms()
        self.get_payment_methods()
        self.get_project_minimum()
        self.get_project_rate()
        self.get_website_url()
        self.get_year_established()
        self.get_workers_compensation()
        self.get_written_contract()
        self.get_location()
        self.get_all_images()
        self.company_page.quit()

    def __del__(self):
        pass

        ## get company name
        # self.company_info["shop_name"] = self.get_company_name()

        ## get category of the company
        # self.company_info["category_name"] = self.get_categories()
