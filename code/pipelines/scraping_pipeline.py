import logging
from ..scraping.webscraper_main import Webscraper

logger = logging.getLogger(__name__)

def run_scraping(final_dir, temp_dir, prev_scraped_path, IS_CI = False):
    logger.debug(f'Final directory: {final_dir}')
    logger.debug(f'Temp directory: {temp_dir}')
    logger.debug(f'Previous scraped path: {prev_scraped_path}')

    final_columns = [
    'title', 'pet', 'brand', 'size', 'quantity', 'price', 'sale_price', 'delivery_info', 'available',
    'website', 'category', 'page_number', 'product_number',
    'product_link', 'category_link', 'error'
    ]

    scraper = Webscraper(
        final_columns=final_columns,
        final_output_path=final_dir,
        temp_output_path=temp_dir,
        prev_scraped_path=prev_scraped_path
    )

    try:

        result_df = scraper.run_webscraper(
            website_type_dict=get_website_scrape_types(),
            max_pages=10,
            skip_scraped_products=False,
            skip_scraped_categories=False,
            IS_CI=IS_CI
        )

        logging.info(f"Scraping completed. Rows scraped: {len(result_df)}")
    except Exception:
        logging.error("Scraper failed.")
        raise

def get_website_scrape_types():
    return {
        'dierapotheker': 'product',
        'hondenkattenapotheek': 'category',
        'pharmacy4pets': 'product',
        'medpets': 'product',
        'petmarkt': 'product',
    }