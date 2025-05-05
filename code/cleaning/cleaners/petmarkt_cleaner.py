import pandas as pd
from .base_cleaner import BaseCleaner


class PetmarktCleaner(BaseCleaner):

    def fill_size(self):

        def get_size(row):

            brand = str(row.get("brand", "").lower())
            size = row["size"]

            if not pd.isna(size):
                return size
            elif "panacur" in brand:
                return row["quantity_package"]
            else:
                return size

        self.df_cleaned["size"] = self.df_orig.apply(get_size, axis=1)
        return self


    def fill_quantity_package(self):

        def get_quantity(row):

            brand = str(row.get("brand", "").lower())
            quantity = row["quantity_package"]

            if not pd.isna(quantity):
                return quantity
            elif "milbemax" in brand or "drontal" in brand:
                return row["title"]
            elif "seresto" in brand:
                return row["size"]
            else:
                return row["quantity_package"]

        self.df_cleaned["quantity_package"] = self.df_orig.apply(get_quantity, axis=1)
        return self


    def fill_quantity_ordered(self):

        def get_quantity(row):
            
            brand = str(row.get("brand", "").lower())
            quantity_ordered = row["quantity_ordered"]

            if not quantity_ordered == 1:
                return quantity_ordered
            elif "milbemax" in brand or "drontal" in brand or "seresto" in brand:
                return row["title"]
            return row["quantity_package"]

        self.df_cleaned["quantity_ordered"] = self.df_orig.apply(get_quantity, axis=1)
        return self
