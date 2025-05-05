import pandas as pd
from .base_cleaner import BaseCleaner


class HondenkattenapotheekCleaner(BaseCleaner):

    def fill_size(self):

        def get_size(row):

            brand = str(row.get("brand", "").lower())
            size = row["size"]
            return size

        self.df_cleaned["size"] = self.df_orig.apply(get_size, axis=1)
        return self


    def fill_quantity_package(self):

        def get_quantity(row):

            brand = str(row.get("brand", "").lower())
            quantity = row["quantity_package"]
            return quantity

        self.df_cleaned["quantity_package"] = self.df_orig.apply(get_quantity, axis=1)
        return self


    def fill_quantity_ordered(self):

        def get_quantity(row):

            brand = str(row.get("brand", "").lower())
            quantity_ordered = row["quantity_ordered"]
            
            if not quantity_ordered == 1:
                return quantity_ordered
            return row["quantity_package"]

        self.df_cleaned["quantity_ordered"] = self.df_orig.apply(get_quantity, axis=1)
        return self
