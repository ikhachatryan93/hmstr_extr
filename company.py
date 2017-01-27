

class HomestarCompanyInfo:
    COMPANY_RESULTS_CSS_CLASS = "company-result"
    COMPANY_URL_CSS_CLASS = "company-result__name"
    COMPANY_CATEGORY_CSS_CLASS = "company-result__categories"

    def __init__(self):
        self.company_info = dict(
            url_id="", url_name="", category_id="", category_name="", keyword="",
            keyword_name="", shop_id="", shop_name="", shop_logo="", contact_person_name="",
            phone="", country_id="", country_name="", province="", city="", location="",
            address="", year_established="", no_of_employees="", payment_method="", licenses="",
            workers_compensation="", is_bounded="", warranty_terms="", written_contract="",
            project_rate="", project_minimum="", liability_insurance="", website="", homestars_star_score="",
            homestars_rating="", homestars_total_reviews="", homestars_review_id="", homestars_reviews=[],
            homestars_review_user_id="", homestars_review_user_name="", homestars_review_date="",
            homestars_review_location="", shop_photos="", shop_profile_id="", shop_profile_desc="")

    def add_info(self, key, value):
        self.company_info[key] = value
