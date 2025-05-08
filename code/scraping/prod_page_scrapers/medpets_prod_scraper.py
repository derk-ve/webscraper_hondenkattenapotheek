from selenium.webdriver.common.by import By
from .base_prod_scraper import BaseProdScraper
from ...scraping.configs.xpath_configs import product_xpath
import pandas as pd
import json
import re


class MedpetsProdScraper(BaseProdScraper):

    def _scrape_product_page(self) -> dict:

        product = self.driver.find_element(By.XPATH, "//" + product_xpath[self.website]["product_element"])
        product_json_content = re.search(r"window\.dataLayer\.push\((\{.*?\})\);", product.get_attribute("textContent")).group(1)
        data = json.loads(product_json_content)
        products = data.get("products", [])
        product_rows = []

        for i, product in enumerate(products):
            product_row = {}
            product_row["title"] = product.get("name")
            descr = product.get("dimension2").split(" - ")
            self._split_descr(product_row, descr)

            price = product.get("unit_price")
            sale_price = product.get("unit_sale_price") if product.get("unit_sale_price") != price else pd.NA

            product_row["price"] = price
            product_row["sale_price"] = sale_price
            product_rows.append(product_row)

        return product_rows


    def _split_descr(self, product_row, descr):

        product_row["brand"] = descr[0]

        if len(descr) == 2:
            product_row["quantity"] = descr[1]

        if len(descr) == 3:
            product_row["size"] = descr[1]
            product_row["quantity"] = descr[2]

        return product_row
