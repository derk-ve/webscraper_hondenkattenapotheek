import os
import datetime
import logging
import argparse
from code.utils.logger import setup_logger
from code.pipelines.scraping_pipeline import run_scraping
from code.pipelines.cleaning_pipeline import run_cleaning
from code.pipelines.result_pipeline import build_result_file
from code.pipelines.comparison_pipeline import compare_results

IS_CI = os.getenv("GITHUB_ACTIONS") == "true"

if IS_CI:
    DATA_DIR = os.path.join(os.getcwd(), "data")  # Relative path in CI
else:
    DATA_DIR = "C:/Users/derkv/OneDrive/Documenten/Brightminds/Webscraper/data"

SCRAPED_DIR = os.path.join(DATA_DIR, "scraped_data")
TEMP_SCRAPED_DIR = os.path.join(SCRAPED_DIR, "temp_results")
FINAL_SCRAPED_DIR = os.path.join(SCRAPED_DIR, "scraped_results")

CLEANED_DIR = os.path.join(DATA_DIR, "cleaned_data")

RESULT_DIR = os.path.join(DATA_DIR, "result_data")

COMPARISON_DIR = os.path.join(DATA_DIR, "comparison_data")

LOG_DIR = os.path.join(os.path.dirname(__file__), "logs")
LOG_FILE = os.path.join(LOG_DIR, "scraper_log.txt")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Run webscraper and/or cleaner.")
    parser.add_argument('--log-level', default='INFO', help="Logging level: DEBUG, INFO, WARNING, ERROR, CRITICAL")
    parser.add_argument('--prev-scraped-path', default=None, help="Optional path to a previous scraped .pkl file")
    parser.add_argument('--skip-scraping', action='store_true', help="Skip scraping and only run cleaning")
    parser.add_argument('--clean-date', help="Date (dd_mm_yyyy) of the file to clean, e.g. 02_05_2025")
    parser.add_argument('--compare-to', help="Compare today's result to this date (format: dd_mm_yyyy)")
    return parser.parse_args()

def ensure_directories():
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(SCRAPED_DIR, exist_ok=True)
    os.makedirs(TEMP_SCRAPED_DIR, exist_ok=True)
    os.makedirs(FINAL_SCRAPED_DIR, exist_ok=True)
    os.makedirs(CLEANED_DIR, exist_ok=True)
    os.makedirs(RESULT_DIR, exist_ok=True)
    os.makedirs(COMPARISON_DIR, exist_ok=True)

def determine_prev_scraped_path(user_provided_path):

    if user_provided_path:

        logging.info(f"Using provided previous scraped path: {user_provided_path}")

        return user_provided_path
    
    logging.info(f"Continuing with no previous scraped file provided")
    return None


def run_webscraper_pipeline(args, run_date_str):
    if args.skip_scraping:
        logging.info('')
        logging.info("Skipping scraping. Proceeding to cleaning only...")
        return None

    prev_scraped_path = determine_prev_scraped_path(args.prev_scraped_path)

    logging.info('')
    logging.info("Starting webscraper...")

    try:

        run_scraping(
            final_dir=FINAL_SCRAPED_DIR,
            temp_dir=TEMP_SCRAPED_DIR,
            prev_scraped_path=prev_scraped_path,
            IS_CI=IS_CI,
        )

        logging.info("Webscraper completed successfully.")

    except Exception:

        logging.error("Failed to scrape and store scraped data.")

        raise

    return os.path.join(FINAL_SCRAPED_DIR, f"scraped_results_full_result_{run_date_str}.pkl")


def run_cleaning_pipeline(run_date_str):
    try:

        logging.info('')
        logging.info('Cleaning scraped data...')

        run_cleaning(FINAL_SCRAPED_DIR, CLEANED_DIR, run_date_str)

        logging.info("Cleaning completed successfully.")

    except Exception:

        logging.error("Failed to clean the scraped data.")

        raise


def run_result_pipeline(run_date_str):

    try:

        logging.info('')
        logging.info("Generating result file...")

        build_result_file(run_date_str, CLEANED_DIR, RESULT_DIR)

    except Exception:

        logging.error("Failed to generate result file.")

        raise

def run_comparison_pipeline(args, run_date_str):
    old_date = args.compare_to

    try:

        logging.info('')
        logging.info("Starting result comparison...")

        compare_results(
            result_dir=RESULT_DIR,
            comparison_dir=COMPARISON_DIR,
            new_date=run_date_str,
            old_date=old_date,
        )

        logging.info("Comparison completed successfully.")

    except Exception:
        
        logging.info('')
        logging.error("Comparison step failed.")

        raise

def main():

    args = parse_arguments()
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)

    setup_logger(log_level=log_level)

    logging.info("Main process started.")
    logging.info(f"Log level set to: {args.log_level.upper()}")

    ensure_directories()

    today_str = datetime.date.today().strftime('%d_%m_%Y')
    run_date_str = args.clean_date or today_str

    try:

        run_webscraper_pipeline(args, run_date_str)

        run_cleaning_pipeline(run_date_str)

        run_result_pipeline(run_date_str)

        run_comparison_pipeline(args, run_date_str)

    except Exception:

        logging.exception("Pipeline execution failed.")

        return

    logging.info('')
    logging.info("Main process completed.")

if __name__ == "__main__":
    main()


