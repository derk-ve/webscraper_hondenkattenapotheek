from ...scraping.utils.mover import Mover
from ...scraping.utils.waiter import Waiter
from ...scraping.configs.xpath_configs import category_xpath
from selenium.webdriver.common.by import By
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class BaseCatScraper:

    def __init__(self, driver, website, final_columns, max_pages=None, prev_scraped_df=None, skip_scraped_products=False):
        self.driver = driver

        self.website = website

        self.final_columns = final_columns

        self.max_pages = max_pages
        self.page_count = None

        self.all_product_info = []
        self.prev_scraped_df = prev_scraped_df
        self.skip_scraped_products = skip_scraped_products

        self.waiter = Waiter(driver)
        self.mover = Mover(driver, website, self.waiter)


    def scrape_category(self, category_url):

        logger.info(f"Going to scrape category: {category_url}...")
        self.driver.get(category_url)

        self.waiter.wait(min=2, max=4, webelement_xpath="//" + category_xpath[self.website]["product_element"])

        self.mover.check_and_click_coockie()

        self._scrape_category_pages(category_url)

        logger.info('')
        return self.all_product_info


    def _scrape_category_pages(self, category_url):

        pagination_handler = CategoryPaginationHandler(self)
        self.page_count = 1

        while True:

            logger.info(f"Scraping page {self.page_count} of {category_url}")
            self.waiter.wait(min=2, max=4, webelement_xpath="//" + category_xpath[self.website]["product_element"])

            self._scrape_category_page_products(category_url)

            logger.info(f"Scraped page {self.page_count} of {category_url}")

            if not pagination_handler.next_page_exists():
                break

            self.mover.go_to_next_page()
            self.page_count += 1

            logging.info('')


    def _scrape_category_page_products(self, category_url: str):

        page_prod_handler = CategoryPageProductHandler(self)
        products = self._extract_product_elements()

        if not products:
            logger.warning(f"No products found on page {self.page_count}")
            return []

        try:

            for i, product in enumerate(products):
                logging.info(f"Going to scrape product {i+1} on page {self.page_count}")
                if page_prod_handler._is_already_scraped_product(product, i+1):
                    continue

                product_info = self._scrape_product_info(product, category_url)
                product_info = page_prod_handler._add_page_metadata(product_info, category_url, i+1)
                self.all_product_info.append(product_info)
                self._log_product_info(product_info)

        except Exception as e:
            logger.error(f"Error scraping product {i+1} on page {self.page_count}: {e}")
            raise


    def _scrape_product_info(self, product, category_url):
        raise NotImplementedError("Each website scraper must implement `_scrape_product_info`.")


    def _extract_product_elements(self):
        return self.driver.find_elements(By.XPATH, "//" + category_xpath[self.website]["product_element"])
    
    def _log_product_info(self, product_info):
        logger.info(f"Product info: {product_info}")


class CategoryPaginationHandler:
    """Handles pagination for category pages."""

    def __init__(self, scraper: BaseCatScraper):
        self.scraper = scraper


    def next_page_exists(self):

        if self.scraper.page_count >= self.scraper.max_pages:
            logging.info(f"Could not go to next page: Reached max page limit: {self.scraper.max_pages}")
            return False

        try:
            self.scraper.mover.get_next_button()
            return True

        except Exception:
            logging.info("Could not go to next page: Could not find next button")
            return False


class CategoryPageProductHandler:
    """Handles extracting product information from category pages."""

    def __init__(self, scraper: BaseCatScraper):
        self.scraper = scraper


    def _is_already_scraped_product(self, product, product_count):

        product_unique_identifier = product.find_element(By.XPATH, ".//" + category_xpath[self.scraper.website]['product_title']).get_attribute("href")

        if self.scraper.prev_scraped_df is not None and not self.scraper.prev_scraped_df.empty and self.scraper.skip_scraped_products and product_unique_identifier in self.scraper.prev_scraped_df["title"].values:
            logging.debug(f"Skipping product {product_count} on page {self.scraper.page_count} with unique identifier: {product_unique_identifier}")
            return True

        return False


    def _add_page_metadata(self, product_info, category_url, product_count):

        product_info["page_number"] = self.scraper.page_count
        product_info["product_number"] = product_count
        product_info["category_link"] = category_url if category_url else pd.NA
        product_info["website"] = self.scraper.website
        product_info = {col: product_info.get(col, pd.NA) for col in self.scraper.final_columns}
        return product_info
