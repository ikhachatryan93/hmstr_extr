#! /bin/env python
import utilities
import homestars

keywords = ["carpet"]
homestars_search_query = "https://homestars.com/companies/search?utf8=%E2%9C%93&search%5Bquery%5D=KEYWORD"


def extract(url_query):
    #browser= utilities.setup_phantomjs_browser(maximize=True)
    browser = utilities.setup_chrome_browser(maximize=True)
    utilities.open_url(url_query, browser)
    browser.save_screenshot("start.png")
    extracted_services = homestars.extract_category(browser)
    #utilities.save_as_jquery(extracted_services)
    #print(len(extracted_services))


def main():
    for keyword in keywords:
        url_query = homestars_search_query.replace("KEYWORD", keyword)
        extract(url_query)

if __name__ == "__main__":
    main()
