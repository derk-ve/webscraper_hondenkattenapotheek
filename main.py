import os
import re
import glob
import datetime
import logging
import argparse
from code.utils.logger import setup_logger
from code.pipelines.scraping_pipeline import run_scraping
from code.pipelines.cleaning_pipeline import run_cleaning
from code.pipelines.result_pipeline import build_result_file
from code.pipelines.comparison_pipeline import compare_results
from code.pipelines.changes_summary_pipeline import create_summary

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


def get_latest_result_file_date() -> str:

    result_files = glob.glob(os.path.join(RESULT_DIR, "result_*.xlsx"))
    date_pattern = re.compile(r"result_(\d{2}_\d{2}_\d{4})\.xlsx")

    dates = []

    for path in result_files:

        logging.info(f"Checking file: {path}")
        match = date_pattern.search(os.path.basename(path))

        if match:
            dates.append(match.group(1))

    if not dates:
        raise ValueError("No valid result files found with date pattern in result_data folder.")

    # Sort dates as datetime objects
    dates_sorted = sorted(dates, key=lambda d: datetime.datetime.strptime(d, "%d_%m_%Y"))

    latest_index = -1 if IS_CI else -2

    if abs(latest_index) > len(dates_sorted):
        raise ValueError(f"Cannot select result file at index {latest_index}: only {len(dates_sorted)} files available.")

    return dates_sorted[latest_index]  # Most recent


def run_webscraper_pipeline(args):

    if args.skip_scraping:
        logging.info('')
        logging.info("Skipping scraping. Proceeding to cleaning only...")
        return 

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



def run_cleaning_pipeline(run_date:str):
    try:

        logging.info('')
        logging.info('Cleaning scraped data...')

        run_cleaning(
            scraped_result_dir=FINAL_SCRAPED_DIR,
            cleaned_dir=CLEANED_DIR,
            date_str=run_date
        )
        
        logging.info("Cleaning completed successfully.")

    except Exception:

        logging.error("Failed to clean the scraped data.")

        raise


def run_result_pipeline(run_date:str):

    try:

        logging.info('')
        logging.info("Generating result file...")

        build_result_file(
            date_str=run_date,
            cleaned_dir=CLEANED_DIR,
            result_dir=RESULT_DIR
        )

    except Exception:

        logging.error("Failed to generate result file.")

        raise

def run_comparison_pipeline(run_date:str, compare_date:str):

    try:

        logging.info('')
        logging.info("Starting result comparison...")

        compare_results(
            result_dir=RESULT_DIR,
            comparison_dir=COMPARISON_DIR,
            new_date=run_date,
            old_date=compare_date,
        )

        logging.info("Comparison completed successfully.")

    except Exception:
        
        logging.info('')
        logging.error("Comparison step failed.")

        raise

def run_changes_summary_pipeline(run_date, compare_date):
    try:

        logging.info('')
        logging.info("Starting changes summary...")

        create_summary(
            comparison_dir=COMPARISON_DIR,
            new_date=run_date,
            old_date=compare_date,
        )

        logging.info("Changes summary completed successfully.")

    except Exception:
        
        logging.info('')
        logging.error("Changes summary step failed.")

        raise

def main():

    args = parse_arguments()
    log_level = getattr(logging, args.log_level.upper(), logging.INFO)

    setup_logger(log_level=log_level)

    logging.info("Main process started.")
    logging.info(f"Log level set to: {args.log_level.upper()}")

    logging.info(f"Scraped data directory: {SCRAPED_DIR}")
    logging.info(f"Main scraped data directory: {SCRAPED_DIR}")
    logging.info(f"Temporary scraped data directory: {TEMP_SCRAPED_DIR}")
    logging.info(f"Final scraped data directory: {FINAL_SCRAPED_DIR}")
    logging.info(f"Cleaned data directory: {CLEANED_DIR}")
    logging.info(f"Result data directory: {RESULT_DIR}")
    logging.info(f"Comparison data directory: {COMPARISON_DIR}")
    logging.info(f"Log directory: {LOG_DIR}")


    ensure_directories()

    today_str = datetime.date.today().strftime('%d_%m_%Y')

    logging.info(f"Today's date: {today_str}")

    run_date = args.clean_date or today_str
    compare_date = args.compare_to or get_latest_result_file_date()


    logging.info(f"Run date: {run_date}")
    logging.info(f"Compare date: {compare_date}")

    try:

        run_webscraper_pipeline(args)

        run_cleaning_pipeline(run_date)

        run_result_pipeline(run_date)

        run_comparison_pipeline(run_date, compare_date)

    except Exception:

        logging.exception("Pipeline execution failed.")

        return

    logging.info('')
    logging.info("Main process completed.")

if __name__ == "__main__":
    main()


