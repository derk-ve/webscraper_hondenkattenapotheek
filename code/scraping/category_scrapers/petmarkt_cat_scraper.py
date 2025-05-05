from .base_cat_scraper import BaseCatScraper
from ..configs.xpath_configs import category_xpath
from selenium.webdriver.common.by import By
import pandas as pd
import re


class DierapothekerCatScraper(BaseCatScraper):

    def _scrape_product_info(self, product, category_url) -> dict:

        product_text = product.text
        product_text_list = product_text.split("\n")
        delivery_info = product.find_element(By.XPATH, ".//" + category_xpath["petmarkt"]["product_delivery_info"]).text
        product_title = product.find_element(By.XPATH, ".//" + category_xpath["petmarkt"]["product_title"]).text
        product_href = product.find_element(By.XPATH, ".//" + category_xpath["petmarkt"]["product_title"]).get_attribute("href")
        product_price = [re.search(r"(\d+,\d+)", l).group(1).replace(",", ".") for l in product_text_list if "€" in l][0]

        product_info_dict = {
            "title": product_title,
            "price": product_price,
            "delivery_info": delivery_info,
            "pet": re.search(r"\.nl/(.*?)/", category_url).group(1),
            "category": category_url.split("/")[-1],
            "product_link": product_href,
        }

        return product_info_dict

