from selenium import webdriver
from .prod_page_scrapers.pharmacy4pets_prod_scraper import Pharmacy4petsProdScraper
from .prod_page_scrapers.medpets_prod_scraper import MedpetsProdScraper
from .prod_page_scrapers.petmarkt_prod_scraper import PetmarktProdScraper
from .prod_page_scrapers.dierapotheker_prod_scraper import DierapothekerProdScraper
from .category_scrapers.dierapotheker_cat_scraper import DierapothekerCatScraper
from .category_scrapers.hondenkattenapotheek_cat_scraper import HondenkattenapotheekCatSraper
from .configs.product_urls import product_urls
from .configs.category_urls import category_urls
from .utils.saver import Saver
import logging
import pandas as pd


logging.basicConfig(level=logging.INFO)


class Webscraper:

    def __init__(self,
                 final_columns,
                 final_output_path,
                 temp_output_path,
                 prev_scraped_path=None):

        self.chrome_options = self._get_chrome_options()
        self.driver = None

        self.prev_scraped_df = pd.read_pickle(prev_scraped_path) if prev_scraped_path else None

        self.final_columns = final_columns
        self.all_products_info = []

        self.saver = Saver(final_output_path, temp_output_path, final_columns)


    def __del__(self):

        self.driver.quit()


    def run_webscraper(self,
                       website_type_dict: dict,
                       max_pages=10,
                       skip_scraped_products=True,
                       skip_scraped_categories=True):

        self.driver = webdriver.Chrome(options=self.chrome_options)

        for website, type in website_type_dict.items():
            print(f"\n\nSCRAPING WEBSITE: {website} WITH SCRAPING TYPE: {type}")

            if type == "product":
                self.all_products_info.extend(self._scrape_product_pages(
                    website=website,
                    skip_scraped_products=skip_scraped_products
                ))

            elif type == "category":
                self.all_products_info.extend(self._scrape_category_pages(
                    website=website,
                    max_pages=max_pages,
                    skip_scraped_products=skip_scraped_products,
                    skip_scraped_categories=skip_scraped_categories
                ))

            else:
                print(f"Non existing scrape type for website: {website}")

        prev_scraped_df = self.prev_scraped_df if skip_scraped_products or skip_scraped_categories else None

        result_df = self.saver.save_full_result_file(
            self.all_products_info,
            prev_scraped_df
        )

        self.driver.quit()
        return result_df


    def _get_product_scraper(self,
                             website):

        scrapers = {
            "pharmacy4pets": Pharmacy4petsProdScraper(self.driver, website, self.final_columns),
            "petmarkt": PetmarktProdScraper(self.driver, website, self.final_columns),
            "medpets": MedpetsProdScraper(self.driver, website, self.final_columns),
            "dierapotheker": DierapothekerProdScraper(self.driver, website, self.final_columns)
        }

        return scrapers.get(website, None)


    def _get_category_scraper(self,
                              website,
                              max_pages,
                              skip_scraped_products):

        scrapers = {
            "dierapotheker": DierapothekerCatScraper(self.driver, website, self.final_columns, max_pages, self.prev_scraped_df, skip_scraped_products),
            "hondenkattenapotheek": HondenkattenapotheekCatSraper(self.driver, website, self.final_columns, max_pages, self.prev_scraped_df, skip_scraped_products)
        }

        return scrapers.get(website, None)


    def _scrape_product_pages(self,
                              website,
                              skip_scraped_products=False):

        scraper = self._get_product_scraper(website)
        all_product_info = []

        if not scraper:
            logging.warning(f"No scraper found for {website}, skipping...")
            return

        for product_url in product_urls.get(website, []):
            if skip_scraped_products and self._is_scraped_link(product_url):
                logging.info(f"Skipping already scraped product: {product_url}")
                continue

            logging.info(f"Scraping: {product_url}")
            print("Returning product scraped result")
            all_product_info.extend(scraper.scrape_product(product_url))

        return all_product_info


    def _scrape_category_pages(self,
                               website,
                               max_pages=10,
                               skip_scraped_products=False,
                               skip_scraped_categories=False):

        """Scrapes all categories for the given websites, handling pagination."""
        all_category_info = []

        scraper = self._get_category_scraper(website, max_pages, skip_scraped_products)

        if not scraper:
            logging.warning(f"No category scraper found for {website}")
            return

        for category_url in category_urls.get(website, []):
            if skip_scraped_categories and self._is_scraped_link(category_url):
                logging.info(f"Skipping already scraped product: {category_url}")
                continue

            logging.info(f"Scraping category: {category_url}")
            all_category_info.extend(scraper.scrape_category(category_url))

        return all_category_info


    def _is_scraped_link(self,
                         product_url):

        if self.prev_scraped_df is not None:
            if product_url in self.prev_scraped_df["product_link"].dropna().values:
                return True
        else:
            logging.warning("Previously scraped df not found, could not check if product is in previously scraped products")

        return False


    def _get_chrome_options(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--lang=nl-NL')
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--start-fullscreen')
        chrome_options.add_argument('--start-incognito')
        chrome_options.add_argument('--incognito')
        return chrome_options
