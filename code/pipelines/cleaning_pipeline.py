import os
import pandas as pd
import logging
from cleaning.cleaner_main import DataCleaner

def run_cleaning(scraped_result_dir, cleaned_dir, date_str):
    logging.info("Cleaning data...")
    try:
        df = pd.read_pickle(os.path.join(scraped_result_dir, f"scraped_results_full_result_{date_str}.pkl"))
        websites = ['dierapotheker', 'petmarkt', 'medpets', 'pharmacy4pets', 'hondenkattenapotheek']

        cleaned_df = (
            DataCleaner(df, websites)
            .apply_general_cleaning()
            .apply_website_specific_cleaning()
            .add_additional_columns()
            .order_columns()
            .get_cleaned_df()
        )

        cleaned_path = os.path.join(cleaned_dir, f"cleaned_data_{date_str}.xlsx")
        cleaned_df.to_excel(cleaned_path, index=False)
        logging.info(f"Saved cleaned file: {cleaned_path}")
    except Exception:
        logging.error("Cleaning failed.")
        raise
