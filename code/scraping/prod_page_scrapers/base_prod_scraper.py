from scraping.utils.waiter import Waiter
from ..configs.xpath_configs import product_xpath
import pandas as pd
import traceback
import re
import logging

logger = logging.getLogger(__name__)

class BaseProdScraper:

    def __init__(self, driver, website, final_columns):
        self.driver = driver
        self.website = website
        self.final_columns = final_columns

        self.waiter = Waiter(driver)


    def scrape_product(self, product_url):

        try:
            self.driver.get(product_url)

            self.waiter.wait(min=2, max=4, webelement_xpath="//" + product_xpath[self.website]["product_element"])

            product_info = self._scrape_product_page()

            if not isinstance(product_info, list):
                product_info = [product_info]

            for info_dict in product_info:
                info_dict["website"] = self.website
                info_dict["product_link"] = product_url
                info_dict.update({col: info_dict.get(col, pd.NA) for col in self.final_columns})

        except Exception as e:
            tb = traceback.extract_tb(e.__traceback__)
            filename, line_number, func_name, text = tb[-1]

            logger.error(f"Error: {e}\nOccurred in file: {filename}\nWithin function: {func_name}\nLine Number: {line_number}\nCode: {text}")

            info_dict = {
                "website": self.website,
                "product_link": product_url,
                "error": f"Error: {e}\nOccurred in file: {filename}\nWithin function: {func_name}\nLine Number: {line_number}\nCode: {text}"
            }

            product_info = [info_dict]
            raise

        for i, pi in enumerate(product_info):
            logger.debug(f"\nProduct {i+1}: {pi}")

        logger.info("Finished scraping product information.")
        return product_info


    def _scrape_product_page(self):
        raise NotImplementedError("Each website scraper must implement `_scrape_product_page`.")
