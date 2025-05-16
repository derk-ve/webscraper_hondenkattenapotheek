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




def compare_results(result_dir: str, comparison_dir: str, new_date: str, old_date: str = None):
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