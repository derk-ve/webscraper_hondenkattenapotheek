from .base_prod_scraper import BaseProdScraper
from scraping.configs.xpath_configs import product_xpath
import pandas as pd
import re
from selenium.webdriver.common.by import By


class DierapothekerProdScraper(BaseProdScraper):

    def _scrape_product_page(self) -> dict:

        product = self.driver.find_element(By.XPATH, "//" + product_xpath[self.website]["product_element"])
        product_text = product.text
        product_text_list = product_text.split("\n")

        # product_saving_header = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_savings_header"])
        product_amount_input_elements = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_amount"])
        product_main_price = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_main_price"])
        product_main_price_old = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_main_price_old"])
        product_price_container = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_price_container"])
        quantity_price_rows = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_price_row"])

        price_per_quantity = {}
        sale_price_per_quantity = {}

        if product_price_container:
            price_per_quantity["1"] = product_price_container[0].find_element(By.XPATH, ".//" + "div[contains(@class, 'amount')]").text + product_price_container[0].find_element(By.XPATH, ".//" + "div[contains(@class, 'cents')]").text
        elif product_main_price and product_main_price_old:
            price_per_quantity["1"] = re.search(r"(\d+[.,]\d+)", product_main_price_old[0].text).group(1)
            sale_price_per_quantity["1"] = product_main_price[0].find_element(By.XPATH, ".//" + "div[contains(@class, 'amount')]").text + product_main_price[0].find_element(By.XPATH, ".//" + "div[contains(@class, 'cents')]").text
        else:
            price_per_quantity["1"] = product_main_price[0].find_element(By.XPATH, ".//" + "div[contains(@class, 'amount')]").text + product_main_price[0].find_element(By.XPATH, ".//" + "div[contains(@class, 'cents')]").text

        # if product_saving_header and "bespaar" in product_saving_header[0].text:
        #     bespaar = True
        # else:
        #     bespaar = False

        if "bespaar" in product_text:
            bespaar = True
        else:
            bespaar = False

        for quantity_price_row in quantity_price_rows:
            if quantity_price_row.text.strip() and "Aantal" not in quantity_price_row.text:
                clean_text = " ".join(quantity_price_row.text.split())
                quantity_ordered = re.search(r"((^| )\d+ )", clean_text).group(1)
                prices = re.findall(r"\d+(?:.|,)\d+", clean_text)
                
                if bespaar:
                    if len(prices) == 3:
                        sale_price_per_quantity[quantity_ordered] = prices[0]
                        price_per_quantity[quantity_ordered] = prices[1]
                    else:
                        price_per_quantity[quantity_ordered] = prices[0]
                        sale_price_per_quantity = pd.NA
                else:
                    if len(prices) == 2:
                        sale_price_per_quantity[quantity_ordered] = prices[0]
                        price_per_quantity[quantity_ordered] = prices[1]
                    else:
                        price_per_quantity[quantity_ordered] = prices[0]
                        sale_price_per_quantity = pd.NA

        for line in product_text_list:
            if "verz" in line and "grat" not in line:
                delivery_info = line

        title = product.find_element(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_title"]).text

        quantity_selected = [p.find_element(By.XPATH, "./ancestor::div[1]").text.strip() for p in product_amount_input_elements if p.is_selected()]
        quantity = quantity_selected[0] if quantity_selected else title

        return {
            "title": title,
            "brand": product.find_element(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_brand"]).text,
            "price": price_per_quantity,
            "sale_price": sale_price_per_quantity,
            "quantity_options": [p.find_element(By.XPATH, "./ancestor::div[1]").text.strip() for p in product_amount_input_elements],
            "quantity": quantity,
            "delivery_info": delivery_info
        }
