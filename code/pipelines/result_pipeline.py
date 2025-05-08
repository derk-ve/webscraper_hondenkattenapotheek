import os
import logging
import pandas as pd
from ..transforming.price_pivot_builder import PricePivotBuilder


def save_result_to_excel(result, result_file):
    """
    Saves the result DataFrame to an Excel file with formatting.
    """
    with pd.ExcelWriter(result_file, engine='xlsxwriter') as writer:
        result.to_excel(writer, sheet_name='Sheet1', index=False)

        workbook = writer.book
        worksheet = writer.sheets['Sheet1']

        format_2dec = workbook.add_format({'num_format': '0.00'})
        for idx, col in enumerate(result.columns):
            if col.startswith('price') or col.startswith('sale_price'):
                worksheet.set_column(idx, idx, None, format_2dec)

    logging.info(f"Result file created: {result_file}")


def handle_missing_prices(missing_price, result_dir, date_str):
    """
    Handles missing prices by saving them to a separate file if any are found.
    """
    if not missing_price.empty:
        missing_file = os.path.join(result_dir, f"missing_in_result_{date_str}.xlsx")
        missing_price.to_excel(missing_file, index=False)
        logging.warning(f"Some products are missing prices. Logged to: {missing_file}")
    else:
        logging.info("All products have valid prices.")


def build_result_file(date_str: str, cleaned_dir: str, result_dir: str):
    logging.info("Building result file...")

    try:
        cleaned_file_path = os.path.join(cleaned_dir, f"cleaned_data_{date_str}.xlsx")
        df = pd.read_excel(cleaned_file_path)

        pvb = PricePivotBuilder(df)
        result = pvb.build()
        missing_price = pvb.check_missing_prices(result)

        os.makedirs(result_dir, exist_ok=True)
        result_file = os.path.join(result_dir, f"result_{date_str}.xlsx")

        save_result_to_excel(result, result_file)
        handle_missing_prices(missing_price, result_dir, date_str)

    except Exception:
        logging.error("Failed to build the result file.")
        raise
