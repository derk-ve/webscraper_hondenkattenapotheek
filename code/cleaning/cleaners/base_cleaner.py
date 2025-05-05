import pandas as pd
from ..configs.dtypes import dtype_map
from ..configs.column_configs import column_order, column_map
from ..string_extractors.string_extractor import StringExtractor
import re


class BaseCleaner:

    def __init__(self,
                 df_orig,
                 df_cleaned=None):

        self.df_orig = df_orig.copy()
        self.df_cleaned = df_cleaned.copy() if isinstance(df_cleaned, pd.DataFrame) else df_orig


    def transform_price_dicts_to_lists(self):

        self.df_cleaned["sale_price"] = self.df_cleaned["sale_price"].apply(
            lambda x: pd.NA if x == {} else x
        )

        self.df_cleaned = self.df_cleaned.assign(
            quantity_ordered=self.df_cleaned["price"].apply(lambda d: list(d.keys()) if isinstance(d, dict) else 1),
            price=self.df_cleaned["price"].apply(lambda d: list(d.values()) if isinstance(d, dict) else d),
            sale_price=self.df_cleaned["sale_price"].apply(lambda d: list(d.values()) if isinstance(d, dict) else d)
        )

        return self


    def explode_price_lists(self):

        price_is_list = self.df_cleaned["price"].apply(lambda x: isinstance(x, list))
        sale_is_list = self.df_cleaned["sale_price"].apply(lambda x: isinstance(x, list))

        df_both = self.df_cleaned[price_is_list & sale_is_list].explode(["price", "sale_price", "quantity_ordered"])
        df_price_only = self.df_cleaned[price_is_list & ~sale_is_list].explode(["price", "quantity_ordered"])
        df_sale_only = self.df_cleaned[~price_is_list & sale_is_list].explode(["sale_price", "quantity_ordered"])
        df_none = self.df_cleaned[~price_is_list & ~sale_is_list]

        self.df_cleaned = pd.concat([df_both, df_price_only, df_sale_only, df_none], ignore_index=True)

        return self


    def clean_price_columns(self):

        for col in self.df_cleaned.columns:
            if col in ["price", "sale_price"]:
                self.df_cleaned[col] = (
                    self.df_cleaned[col]
                    .astype(str)
                    .str.strip()
                    .str.replace(r"[^\d,.-]", "", regex=True)
                    .str.replace(",", ".")
                )

        return self


    def set_dtypes(self):

        for col, dtype in dtype_map.items():
            if col in self.df_cleaned.columns:
                if dtype in ["float", "Int64"]:
                    self.df_cleaned[col] = pd.to_numeric(self.df_cleaned[col], errors="coerce").astype(dtype)
                else:
                    self.df_cleaned[col] = self.df_cleaned[col].astype(dtype)

        self.df_cleaned = self.df_cleaned.mask(self.df_cleaned.isna(), pd.NA)

        return self


    def set_columns_order(self):

        self.df_cleaned = self.df_cleaned[column_order]
        return self


    def rename_columns(self):

        self.df_cleaned = self.df_cleaned.rename(columns=column_map)
        return self


    def set_brand(self):

        def map_brand(brand):
            brand = str(brand).lower()
            for key in ["milbemax", "advantix", "milbactor", "milpro", "drontal", "panacur", "seresto", "vectra"]:
                if key in brand:
                    return key
            if "virbac" in brand:
                return "milpro"
            elif "dronspot" in brand:
                return "drontal"
            print(f"Could not find any specified key in brand: {brand}")
            return pd.NA

        self.df_cleaned["brand"] = self.df_cleaned["brand"].apply(map_brand)
        return self


    def set_size(self):

        def extract_size(row):
            size_to_extract = row["size"]
            if pd.isna(size_to_extract):
                print(f"Can not extract size from non string: {size_to_extract}")
                return pd.NA
            brand = str(row.get("brand", "")).lower()
            extractor_key = brand + "_size"
            animal = row["pet"]
            return StringExtractor.extract(extractor_key, size_to_extract, animal)

        self.df_cleaned["size"] = self.df_cleaned.apply(extract_size, axis=1).astype("category")
        return self


    def set_quantity_package(self):

        def extract_quantity(row):
            quantity_to_extract = row["quantity_package"]
            brand = str(row.get("brand", "")).lower()
            if not isinstance(quantity_to_extract, str):
                return quantity_to_extract
            extractor_key = brand + "_quantity_package"
            animal = row["pet"]
            return StringExtractor.extract(extractor_key, quantity_to_extract, animal)

        self.df_cleaned["quantity_package"] = self.df_cleaned.apply(extract_quantity, axis=1).astype("category")
        return self


    def set_quantity_ordered(self):

        def extract_quantity(row):
            quantity_to_extract = row["quantity_ordered"]
            brand = str(row.get("brand", "")).lower()
            if not isinstance(quantity_to_extract, str):
                return quantity_to_extract
            extractor_key = brand + "_quantity_ordered"
            animal = row["pet"]
            return StringExtractor.extract(extractor_key, quantity_to_extract, animal)

        self.df_cleaned["quantity_ordered"] = self.df_cleaned.apply(extract_quantity, axis=1).astype("category")
        return self
    
    def set_product_name(self):
        self.df_cleaned['product_name'] = self.df_cleaned["pet"].astype(str) + " | " + self.df_cleaned["brand"].astype(str) + " | " + self.df_cleaned["size"].astype(str) + " | " + self.df_cleaned["quantity_package"].astype(str) + " " + self.df_cleaned["quantity_package_unit"].astype(str) 
        return self

    def split_quantity_package(self):

        self.df_cleaned[["quantity_package", "quantity_package_unit"]] = self.df_cleaned["quantity_package"].str.split(" ", n=1, expand=True)
        self.df_cleaned["quantity_package"] = pd.to_numeric(self.df_cleaned["quantity_package"].str.replace(",", "."), errors="coerce")
        return self


    def set_to_total_price(self):

        websites_without_total_price = ["dierapotheker"]
        mask = self.df_cleaned["website"].isin(websites_without_total_price)
        self.df_cleaned.loc[mask, "price"] = self.df_cleaned.loc[mask, "price"] * self.df_cleaned.loc[mask, "quantity_ordered"].round(2).astype("float64")
        self.df_cleaned.loc[mask, "sale_price"] = self.df_cleaned.loc[mask, "sale_price"] * self.df_cleaned.loc[mask, "quantity_ordered"].round(2).astype("float64")
        return self


    def set_pet(self):

        def extract_pet(row):
            title = str(row["title"]).lower() if pd.notna(row["title"]) else ""
            url = (str(row["product_link"]) if pd.notna(row["product_link"]) else
                   str(row["category_link"]) if pd.notna(row["category_link"]) else "").lower()

            exception_words = ["hondenkattenapotheek", "subcat"]
            for exc_word in exception_words:
                url = url.replace(exc_word, "")

            dog_found = any(kw in title or kw in url for kw in ["dog", "hond", "pup", "advantix"]) or re.search(r"\s+hk\s+", title) or re.search(r"\s+kh\s+", title) or "panacur" in title
            cat_found = any(kw in title or kw in url for kw in ["cat", "kat", "kitten"]) or re.search(r"\s+hk\s+", title) or re.search(r"\s+kh\s+", title) or "panacur" in title

            if dog_found and cat_found:
                return "hond & kat"
            elif dog_found:
                return "hond"
            elif cat_found:
                return "kat"
            else:
                return pd.NA

        self.df_cleaned["pet"] = self.df_cleaned.apply(extract_pet, axis=1).astype(str)
        return self


    def fill_size(self):
        """This method should be implemented in a subclass"""
        raise NotImplementedError("Each data cleaner must implement `_scrape_product_page`.")


    def fill_quantity_package(self):
        """This method should be implemented in a subclass"""
        raise NotImplementedError("Each data cleaner must implement `_scrape_product_page`.")


    def fill_quantity_ordered(self):
        """This method should be implemented in a subclass"""
        raise NotImplementedError("Each data cleaner must implement `_scrape_product_page`.")


    def get_df(self):

        return self.df_cleaned

        
