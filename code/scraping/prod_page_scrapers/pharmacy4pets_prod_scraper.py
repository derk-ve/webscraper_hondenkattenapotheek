from .base_prod_scraper import BaseProdScraper
from ..configs.xpath_configs import product_xpath
import time
import re
from selenium.webdriver.common.by import By


class Pharmacy4petsProdScraper(BaseProdScraper):

    def _scrape_product_page(self):

        product = self.driver.find_element(By.XPATH, "//" + product_xpath[self.website]["product_element"])
        title = product.find_element(By.XPATH, ".//" + product_xpath["pharmacy4pets"]["product_title"]).text.strip()
        brand = title.split(" ")[0].strip()
        product_info_rows = self._get_all_rows_by_scrolling(product)
        product_rows = []

        for i, row in enumerate(product_info_rows):
            product_row = {}

            if "€" in row:
                product_row["size"] = [l.split("|")[0].strip() for l in row.split("\n") if "|" in l][0] if "|" in row else row.split("\n")[0]
                product_row["quantity"] = [l.split("|")[-1].strip() for l in row.split("\n") if "|" in l][0] if "|" in row else row.split("\n")[0]
                product_row["price"] = [re.search(r"(\d+(?:,|.)\d+)", l).group(1) for l in row.split("\n") if "€" in l][0]
                product_row["title"] = title
                product_row["brand"] = brand
                product_rows.append(product_row)

        return product_rows


    def _get_all_rows_by_scrolling(self, product):

        unique_rows = set()

        for i in range(4):
            self.driver.execute_script("window.scrollBy(0, 500);")
            time.sleep(2)

            rows = product.find_elements(By.XPATH, ".//" + product_xpath["pharmacy4pets"]["product_row_element"])

            for row in rows:
                if row.text and row.text not in unique_rows:
                    unique_rows.add(row.text)

        return unique_rows
