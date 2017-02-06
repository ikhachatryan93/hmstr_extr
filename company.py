from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
from datetime import datetime
import configparser
import time
import utilities
import logging

logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
rootLogger = logging.getLogger()

log_name = datetime.now().strftime('scraping_%H_%M_%d_%m_%Y.log')
fileHandler = logging.FileHandler(filename=log_name)
fileHandler.setFormatter(logFormatter)
rootLogger.addHandler(fileHandler)
logging.basicConfig(level=logging.DEBUG)

homestars_url = "https://www.homestars.com/"

extract_reviews = True
extract_images = True


def parse_extraction_info_from_config_file():
    config_parser = configparser.RawConfigParser()
    config_file = r'./configs.txt'
    config_parser.read(config_file)

    global extract_reviews
    global extract_images

    extract_reviews = config_parser.getboolean('extraction_info', 'reviews')
    extract_images = config_parser.getboolean('extraction_info', 'images')


class HomestarCompanyInfo:
    COMPANY_RESULTS_CSS_CLASS = "company-result"
    COMPANY_URL_CSS_CLASS = "company-result__name"
    COMPANY_CATEGORY_CSS_CLASS = "company-result__categories"

    def __init__(self, company_url, keyword, browser_name="chrome"):
        self.company_info = dict(
            url_name=company_url, keyword=keyword, shop_name="",
            category_name="", shop_logo="", contact_person_name="",
            country_name="Canada", province="", city="",
            location="", address="", phone="", year_established="",
            number_of_employees="", payment_methods="", licenses="",
            workers_compensation="", is_bonded="", warranty_terms="",
            written_contract="", project_rate="", project_minimum="",
            liability_insurance="", website="", homestars_star_score="",
            homestars_rating="", homestars_total_reviews="", postal_code="",
            homestars_reviews=[], shop_photos_links=[], shop_profile_desc="")

        if "phantomjs" in browser_name:
            self.company_page = utilities.setup_phantomjs_browser(maximize=True)
        else:
            self.company_page = utilities.setup_chrome_browser(maximize=True)

        self.company_page.get(self.company_info["url_name"])
        self.company_page_source = BeautifulSoup(self.company_page.page_source, "html5lib")
        self.company_profile_details = self.company_page_source.find("div", {"class", "company-profile__details"})
        self.company_address_info = self.company_page_source.find("address", {"class": "company-header__address"})
        self.NF = "From {}: could not find ".format(self.company_info["url_name"])
        self.wait_5 = WebDriverWait(self.company_page, 5)
        self.wait_2 = WebDriverWait(self.company_page, 2)
        self.wait_1 = WebDriverWait(self.company_page, 1)

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
            company_name = self.wait_5.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".company-header__name>h1"))).text
        except NoSuchElementException:
            logging.error(self.NF + "company name")
            return

        self.company_info["shop_name"] = company_name.strip()

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
            logging.warning(self.NF + "region")
            return

        self.company_info["province"] = province.get_text().strip(", ")

    def get_city(self):
        try:
            city = self.company_page.find_element_by_css_selector(".city-name").text
        except NoSuchElementException:
            logging.warning(self.NF + "city")
            return

        self.company_info["city"] = city.strip()

    def get_address(self):
        address = self.company_address_info.find("spam", {"itemprop": "streetAddress"})
        if address is None:
            logging.warning(self.NF + "address")
            return

        self.company_info["address"] = address.get_text().strip(", ")

    def get_postal(self):
        postal = self.company_address_info.find("span", {"itemprop": "postalCode"})
        if postal is None:
            logging.warning(self.NF + "postal code")
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

    def get_number_of_reviews(self):
        try:
            num_revs = self.company_page_source.find("span", {"class": "review-aggregate-rating__total"}).find(
                "a").get_text()
        except:
            logging.warning(self.NF + "number of reviews")
            return

        self.company_info["homestars_total_reviews"] = num_revs

    def get_company_logo(self):
        try:
            logo_url = self.company_page_source.find("div", {"class": "company-header__logo"}).find("img")["src"]
        except:
            logging.warning(self.NF + "company logo")
            return

        self.company_info["shop_logo"] = logo_url

    def get_star_score(self):
        try:
            num_revs = self.company_page_source.find("span", {"class": "star-score__score"}).get_text()
        except:
            logging.warning(self.NF + "star score")
            return

        self.company_info["homestars_star_score"] = num_revs

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

    def click_all_read_more_buttons(self):
        time.sleep(0.2)
        try:
            see_more_all = self.company_page.find_elements_by_css_selector(".more-link")
        except NoSuchElementException:
            logging.WARNING(
                "For reviews, see_more elements are not found. url:{}".format(self.company_info["url_name"]))
            return
        except Exception as e:
            error_msg = "Unknown fail while trying to get see_more elements. exception:{}. url:{}"
            logging.error(error_msg.format(str(e), self.company_info["url_name"]))
            return

        for s in see_more_all:
            try:
                time.sleep(0.1)
                self.company_page.execute_script("return arguments[0].scrollIntoView();", s)
                self.company_page.execute_script("return arguments[0].click();", s)
            except Exception as e:
                logging.WARNING("Can not click on see_more elements for reviews: exception: {}".format(str(e)))

    def get_review_list(self, review_list):
        for r in review_list:
            try:
                review = {"review_date": r.find_element_by_css_selector(".review-content__date").text,
                          "review_owner": r.find_element_by_css_selector(".review-author__name>a").text,
                          "review_owner_location": r.find_element_by_css_selector(
                              ".review-author__location").text.strip("\nread less")}
            except Exception as e:
                print("Exception in get_review_list" + str(e))
                continue

            try:
                review_text = r.find_element_by_css_selector(".details").text.strip("\nread less")
            except NoSuchElementException:
                try:
                    review_text = r.find_element_by_css_selector(".expander.review-story__text>p").text.strip("\nread less")
                except NoSuchElementException:
                    self.company_info["homestars_reviews"].append(review)
                    continue
            try:
                response_text = r.find_element_by_css_selector(".review-response__body").text
            except:
                response_text = ""

            review["review_text"] = review_text
            review["response_text"] = response_text
            self.company_info["homestars_reviews"].append(review)

    def get_current_reiew_list(self):
        try:
            review_list = self.company_page.find_elements_by_css_selector(".review-wrap")
        except NoSuchElementException:
            logging.debug('Could not find reviews from {} url'.format(self.company_info["url_name"]))
            return

        self.get_review_list(review_list)

    def wait_page_load(self):
        timeout = time.time() + 4
        while 800 < self.company_page.execute_script("return window.scrollY"):
            time.sleep(0.1)
            if timeout < time.time():
                return

    def get_all_reviews(self):
        self.click_all_read_more_buttons()
        self.get_current_reiew_list()
        try:
            self.company_page.find_element_by_css_selector(".next_page")
        except NoSuchElementException:
            return

        try:
            next_page = self.wait_5.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".next_page")))
        except TimeoutError:
            return

        while "disabled" not in next_page.get_attribute("class"):
            self.company_page.execute_script("return arguments[0].scrollIntoView(false);", next_page)
            next_page.click()
            self.wait_page_load()
            self.click_all_read_more_buttons()
            self.get_current_reiew_list()
            try:
                next_page = self.wait_2.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".next_page")))
            except TimeoutError or NoSuchElementException:
                print("In get_all_reviews, element is not clickable")
                break

        logging.debug("Finishing reviews extraction from {} page: ".format(self.company_info["url_name"]))
        return

    def get_all_images(self):
        try:
            old_url = self.company_page.current_url
            see_more = self.wait_1.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".square-gallery__see"
                                                                                               "-more")))
            self.company_page.execute_script("return arguments[0].scrollIntoView();", see_more[len(see_more) - 1])
            see_more = self.wait_5.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".square-gallery__see-more")))
            self.company_page.execute_script("return arguments[0].click();", see_more)
            while old_url in self.company_page.current_url:
                time.sleep(0.1)
            photos_tags = self.wait_5.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".square"
                                                                                                  "-gallery__link")))
            for p in photos_tags:
                self.company_info['shop_photos_links'].append(p.get_attribute("href"))

            # go back to company main page
            self.company_page.execute_script("window.history.go(-1)")
        except:
            try:
                photos_tags = self.company_page.find_elements_by_css_selector(".square-gallery__link")
                self.company_page.execute_script("return arguments[0].scrollIntoView();", photos_tags[0])
                for p in photos_tags:
                    self.company_info['shop_photos_links'].append(p.get_attribute("href"))
            except:
                logging.warning(self.NF + "photos")

    def extract_company(self):
        #try:
        parse_extraction_info_from_config_file()
        self.get_company_name()
        self.get_address()
        self.get_phone()
        self.get_region()
        self.get_categories()
        self.get_contact_person_name()
        self.get_postal()
        self.get_bonded()
        self.get_city()
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
        self.get_number_of_reviews()
        self.get_star_score()
        self.get_rating()
        self.get_company_logo()
        if extract_images:
            self.get_all_images()
        if extract_reviews:
            self.get_all_reviews()
        #except Exception as e:
        #    self.company_page.save_screenshot("iasd.png")
        #    logging.critical("Exception while extracting {} company. {}".format(self.company_info["url_name"], str(e)))
        self.company_page.quit()
