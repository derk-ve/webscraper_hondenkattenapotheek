from .base_prod_scraper import BaseProdScraper
from selenium.webdriver.support.ui import Select
from webscraper.configs.xpath_configs import product_xpath
import pandas as pd
import re
from selenium.webdriver.common.by import By


class PetmarktProdScraper(BaseProdScraper):

    def _scrape_product_page(self) -> dict:

        product = self.driver.find_element(By.XPATH, "//" + product_xpath[self.website]["product_element"])
        product_text = product.text
        product_text_list = product_text.split("\n")

        available = False if "niet leverbaar" in product_text.lower() else True
        quantity = [l.split(":")[1].strip() for l in product_text_list if "verpakk" in l.lower()][0] if not available and "verpakk" in product.text else pd.NA
        size = pd.NA

        product_quantity_select_divs = product.find_elements(By.XPATH, ".//" + product_xpath["petmarkt"]["product_quantity_size_div"])

        for div in product_quantity_select_divs:
            
            if pd.isna(size) and "gewich" in div.text.lower():
                size = self._get_selected_option(div.find_element(By.XPATH, ".//" + product_xpath["petmarkt"]["product_quantity_size_select"])).text
            elif pd.isna(quantity) and "aant" in div.text.lower():
                quantity = self._get_selected_option(div.find_element(By.XPATH, ".//" + product_xpath["petmarkt"]["product_quantity_size_select"])).text

        return {
            "title": product.find_element(By.XPATH, ".//" + product_xpath["petmarkt"]["product_title"]).text,
            "brand": product.find_element(By.XPATH, ".//" + product_xpath["petmarkt"]["product_title"]).text.split(" ")[0].strip(),
            "price": [re.search(r"(\d+,\d+)", l).group(1).replace(",", ".") for l in product_text_list if "€" in l and "verz" not in l][0],
            "size": size,
            "quantity": quantity,
            "delivery_info": [l for l in product_text_list if "verz" in l][0],
            "available": available
        }


    def _get_selected_option(self, select_element):

        selected_option = Select(select_element).first_selected_option
        return selected_option
