from .base_cat_scraper import BaseCatScraper
from ..configs.xpath_configs import category_xpath
from selenium.webdriver.common.by import By
import re


class HondenkattenapotheekCatSraper(BaseCatScraper):

    def _scrape_product_info(self, product, category_url) -> dict:

        product_text = product.text
        product_text_list = product_text.split("\n")
        title = product.find_element(By.XPATH, ".//" + category_xpath["hondenkattenapotheek"]["product_title"]).text
        product_price = product.find_element(By.XPATH, ".//" + category_xpath["hondenkattenapotheek"]["product_price"]).text

        product_info_dict = {
            "title": title,
            "brand": title,
            "price": re.search(r"(\d+,\d+)", product_price).group(1),
            "quantity": title,
            "size": title,
            # "product_link": product_href,
        }

        return product_info_dict
