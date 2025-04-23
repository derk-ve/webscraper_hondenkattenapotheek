from .base_cat_scraper import BaseCatScraper
from ..configs.xpath_configs import category_xpath
from selenium.webdriver.common.by import By
import pandas as pd
import re


class DierapothekerCatScraper(BaseCatScraper):

    def _scrape_product_info(self,
                             product,
                             category_url) -> dict:

        product_text = product.text
        delivery_info = product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_delivery_info"]).text

        if "alleen" in delivery_info.lower() and "verkrijgbaar" in delivery_info.lower():
            product_price = pd.NA

        else:
            product_amount = product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_price_amount"]).text
            product_cents = product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_price_cents"]).text
            product_price = float(f"{product_amount.replace(',','.')}{product_cents}")

        ex_sale_price = pd.NA

        if product_text.count("€") == 2:
            ex_sale_price_element = product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_price_ex_sale"])
            match = re.search(r"(\d+,\d+)", ex_sale_price_element.text)

            if match:
                ex_sale_price = float(match.group(1).replace(",", "."))

        return {
            "title": product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_title"]).text,
            "brand": product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_brand"]).text,
            "price": product_price,
            "price_ex_sale": ex_sale_price,
            "delivery_info": delivery_info,
            "pet": re.search(r"\.nl/(.*?)/", category_url).group(1),
            "category": category_url.split("/")[-2],
            "product_link": product.find_element(By.XPATH, ".//" + category_xpath["dierapotheker"]["product_title"]).get_attribute("href"),
        }


