import logging
import os
import re
import datetime
import glob
from ..comparing.price_comparer import PriceComparer

def save_comparison_to_excel(diff, new_rows, removed_rows, comparison_dir, comparison_dates):
    """
    Saves the comparison DataFrame to an Excel file.
    """
    diff.to_excel(os.path.join(comparison_dir, "diff_" + comparison_dates + ".xlsx"), index=False)
    new_rows.to_excel(os.path.join(comparison_dir, "new_rows_" + comparison_dates + ".xlsx"), index=False)
    removed_rows.to_excel(os.path.join(comparison_dir, "removed_rows_" + comparison_dates + ".xlsx"), index=False)
    logging.info(f"Comparison file saved: {os.path.join(comparison_dir, 'diff_' + comparison_dates + '.xlsx')}")



def find_latest_result_file_date(result_dir: str) -> str:
    # logging.info(f'looking for files: {os.path.join(result_dir, "result_*.pkl")}')
    result_files = glob.glob(os.path.join(result_dir, "result_*.xlsx"))
    date_pattern = re.compile(r"result_(\d{2}_\d{2}_\d{4})\.xlsx")

    dates = []
    for path in result_files:
        logging.info(f"Checking file: {path}")
        match = date_pattern.search(os.path.basename(path))
        if match:
            dates.append(match.group(1))

    if not dates:
        return None

    # Sort dates as datetime objects
    dates_sorted = sorted(dates, key=lambda d: datetime.datetime.strptime(d, "%d_%m_%Y"))
    return dates_sorted[-2]  # Most recent



def compare_results(result_dir: str, comparison_dir: str, new_date: str, old_date: str = None):
    logging.info(f"Comparing result file from {new_date} to {old_date}...")

    if not old_date:
        old_date = find_latest_result_file_date(result_dir)
        if not old_date:
            raise ValueError("No previous result file found for comparison.")

    logging.info(f"Comparing result file from {new_date} to {old_date}...")

    try:
        old_file = os.path.join(result_dir, f"result_{old_date}.xlsx")
        new_file = os.path.join(result_dir, f"result_{new_date}.xlsx")
        comparer = PriceComparer(old_file, new_file)
        diff, new_rows, removed_rows = comparer.run()

        save_comparison_to_excel(diff, new_rows, removed_rows, comparison_dir, f"{new_date}__{old_date}")

        logging.info(f"Rows changed: {len(diff)}, added: {len(new_rows)}, removed: {len(removed_rows)}")
    except Exception:
        logging.error("Failed to compare result files.")
        raise