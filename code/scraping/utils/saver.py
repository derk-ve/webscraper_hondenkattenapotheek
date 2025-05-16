import pandas as pd
from datetime import datetime
import requests
import logging

logger = logging.getLogger(__name__)

class Saver:

    def __init__(self,
                 final_output_path,
                 temp_output_path,
                 final_columns):

        logging.info("Setting final output path in saver to : {final_output_path}")
        self.final_output_path = final_output_path
        self.temp_output_path = temp_output_path
        self.final_columns = final_columns

        logger.info(f"Final output path: {self.final_output_path}")
        logger.info(f"Temporary output path: {self.temp_output_path}")


    def save_temp_file(self,
                       product_info):

        print(f"\nAdding result to temporary result file...")
        df_temp = pd.DataFrame(product_info)
        df_temp = df_temp[self.final_columns]
        df_temp.to_pickle(self.temp_file_path + ".pkl")
        df_temp.to_excel(self.temp_file_path + ".xlsx", index=False)
        print(f"Temporary results saved to {self.temp_file_path}")


    def save_website_file(self,
                          all_products_info,
                          website,
                          existing_products_df=None):

        print(f"\nSaving {website} result to website result file...")
        df = pd.DataFrame(all_products_info)
        df = df[self.final_columns]

        if existing_products_df:
            df = pd.concat([existing_products_df, df]).drop_duplicates().reset_index(drop=True)

        df_website = df[df["website"] == website]
        output_path = self.final_output_path + f"_{website}"
        output_path = self.add_date_to_file_path(output_path)
        df_website.to_excel(output_path + ".xlsx", index=False)
        df_website.to_pickle(output_path + ".pkl")
        print(f"{website} results saved to {output_path}")


    def save_full_result_file(self,
                              all_products_info,
                              existing_products_df=None):

        print(f"\nSaving full result file...")

        if not all_products_info:
            print("No products scraped, can not create result file")
            return

        df = pd.DataFrame(all_products_info)
        df = df[self.final_columns]

        if existing_products_df is not None:
            print("Concatenating old with new df")
            df = pd.concat([existing_products_df, df])

        df = df.drop_duplicates(subset=["title", "product_link", "size", "quantity", "pet"], keep="first").reset_index(drop=True)
        output_path = self.add_date_to_file_path(self.final_output_path + "_full_result")

        try:
            df.to_excel(output_path + ".xlsx", index=False)
            df.to_csv(output_path + ".csv", index=False, encoding="utf-8")
            df.to_pickle(output_path + ".pkl")
            print(f"Full results saved to {output_path}")
        except Exception as e:
            print("Failed to save result ", e)

        return df


    def add_date_to_file_path(self,
                              file_path):

        date = datetime.now().strftime("%d_%m_%Y")
        return file_path + f"_{date}"


    def send_csv_to_zapier(file_path: str):

        webhook_url = "https://hooks.zapier.com/hooks/catch/22208472/2egbtp9/"
        with open(file_path, "rb") as f:
            files = {"file": f}
            response = requests.post(webhook_url, files=files)

        return response.status_code
