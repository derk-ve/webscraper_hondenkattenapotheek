import pandas as pd
from .base_cleaner import BaseCleaner


class DierapothekerCleaner(BaseCleaner):

    def fill_size(self):

        def get_size(row):

            brand = str(row.get("brand", "").lower())
            size = row["size"]

            if not pd.isna(size):
                return size
            elif "drontal" in brand or "milbemax" in brand:
                return row["title"]
            else:
                return row["quantity_package"]

        self.df_cleaned["size"] = self.df_orig.apply(get_size, axis=1)
        return self


    def fill_quantity_package(self):

        def get_quantity(row):

            brand = str(row.get("brand", "").lower())
            quantity = row["quantity_package"]

            if "milbemax" in brand and "kauw" in row["title"].lower():
                return row["title"] + " " + quantity
            elif not pd.isna(quantity):
                return quantity
            else:
                return row["quantity_package"]

        self.df_cleaned["quantity_package"] = self.df_orig.apply(get_quantity, axis=1)
        return self


    def fill_quantity_ordered(self):

        def get_quantity(row):

            brand = str(row.get("brand", "").lower())
            quantity_ordered = row["quantity_ordered"]
            return quantity_ordered

        self.df_cleaned["quantity_ordered"] = self.df_orig.apply(get_quantity, axis=1)
        return self

        