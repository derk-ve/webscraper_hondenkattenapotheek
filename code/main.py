import os
import datetime
import logging
import argparse
from selenium import webdriver
from webscraper.webscraper_main import Webscraper
from utils.logger import setup_logger

# Final columns
final_columns = [
    'title', 'pet', 'brand', 'size', 'quantity', 'price', 'sale_price', 'delivery_info', 'available',
    'website', 'category', 'page_number', 'product_number',
    'product_link', 'category_link', 'error'
]

# Paths
BASE_PATH = "C:/Users/derkv/OneDrive/Documenten/Brightminds/Webscraper/data/scraped_data"
TEMP_PATH = os.path.join(BASE_PATH, "temp_results")
RESULT_PATH = os.path.join(BASE_PATH, "scraped_results")
LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "scraper_log.txt")

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run webscraper with logging level and input file control.")
    parser.add_argument('--log-level', default='INFO', help="Set logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    parser.add_argument('--prev-scraped-path', default=None, help="Optional: path to previous scraped .pkl file")
    return parser.parse_args()

def ensure_directories():
    os.makedirs(TEMP_PATH, exist_ok=True)
    os.makedirs(RESULT_PATH, exist_ok=True)

def determine_prev_scraped_path(user_provided_path):
    if user_provided_path:
        logging.info(f"Using provided previous scraped path: {user_provided_path}")
        return user_provided_path
    logging.info(f"Continuing with no previous scraped file provided")
    return None

def get_chrome_options():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--lang=nl-NL')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--start-fullscreen')
    chrome_options.add_argument('--start-incognito')
    chrome_options.add_argument('--incognito')
    return chrome_options

def get_website_scrape_types():
    return {
        'dierapotheker': 'product',
        'hondenkattenapotheek': 'category',
        'pharmacy4pets': 'product',
        'medpets': 'product',
        'petmarkt': 'product',
    }

def run_full_scrape(prev_scraped_path):
    logging.info("Starting scraper setup...")
    chrome_options = get_chrome_options()

    scraper = Webscraper(
        chrome_options=chrome_options,
        final_columns=final_columns,
        final_output_path=RESULT_PATH,
        temp_output_path=TEMP_PATH,
        prev_scraped_path=prev_scraped_path
    )

    website_scrape_types = get_website_scrape_types()

    logging.info("Running webscraper on configured websites...")
    try:
        result_df = scraper.run_webscraper(
            website_type_dict=website_scrape_types,
            max_pages=10,
            skip_scraped_products=False,
            skip_scraped_categories=False
        )
        logging.info(f"Scraping completed. Rows scraped: {len(result_df)}")
    except Exception:
        logging.exception("Scraper failed with an exception.")
        raise

def main():
    args = parse_arguments()
    setup_logger(args.log_level)
    logging.info("Main process started.")

    ensure_directories()
    prev_scraped_path = determine_prev_scraped_path(args.prev_scraped_path)
    
    try:
        run_full_scrape(prev_scraped_path)
        logging.info("Main process completed successfully.")
    except Exception:
        logging.exception("Main process failed.")
        print("An error occurred during scraping. Check the log file for details.")

if __name__ == "__main__":
    main()


