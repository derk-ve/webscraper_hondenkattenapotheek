from .cleaners.base_cleaner import BaseCleaner
from .cleaners.dierapotheker_cleaner import DierapothekerCleaner
from .cleaners.petmarkt_cleaner import PetmarktCleaner
from .cleaners.medpets_cleaner import MedpetsCleaner
from .cleaners.pharmacy4pets_cleaner import Pharmacy4petsCleaner
from .cleaners.hondenkattenapotheek_cleaner import HondenkattenapotheekCleaner
import pandas as pd

class DataCleaner:
    def __init__(self, df, websites):
        self.df_orig = df.copy()
        self.df_cleaned = df.copy()
        self.websites = websites

    def clean_scraped_result(self):
        return self.apply_general_cleaning().apply_website_specific_cleaning().add_additional_columns().order_columns().get_cleaned_df()
    
    def apply_general_cleaning(self):
        self.df_cleaned = (
            BaseCleaner(self.df_orig)
            .transform_price_dicts_to_lists()
            .explode_price_lists()
            .clean_price_columns()
            .set_pet()
            .set_dtypes()
            .rename_columns()
            .get_df()
        )
        return self
    
    def _get_website_cleaner(self, website):
        if website == 'dierapotheker':
            return DierapothekerCleaner
        elif website == 'petmarkt':
            return PetmarktCleaner
        elif website == 'medpets':
            return MedpetsCleaner
        elif website == 'pharmacy4pets':
            return Pharmacy4petsCleaner
        elif website == 'hondenkattenapotheek':
            return HondenkattenapotheekCleaner
        else:
            print(f'No cleaner found for website: {website}')

    def apply_website_specific_cleaning(self):
        cleaned_subsets = []
        for website in self.websites:
            print(f'\nDoing website specific cleaning for: {website}')
            df_cleaned_subset = self.df_cleaned[self.df_cleaned['website'] == website].copy()
            cleaner = self._get_website_cleaner(website)
            if df_cleaned_subset.empty or not cleaner:
                print(f'Skipping {website} cleaning')
                continue

            df_cleaned_subset = (
                cleaner(df_cleaned_subset)
                .set_brand()
                .fill_size().set_size()
                .fill_quantity_package().set_quantity_package()
                .fill_quantity_ordered().set_quantity_ordered()
                .split_quantity_package()
                .get_df())
            
            if website == 'dierapotheker':
                df_cleaned_subset = (
                    cleaner(df_cleaned_subset)
                    .set_to_total_price()
                    .get_df())
                
            cleaned_subsets.append(df_cleaned_subset)
        self.df_cleaned = pd.concat(cleaned_subsets, ignore_index=True)
        return self
    
    def add_additional_columns(self):
        self.df_cleaned = BaseCleaner(self.df_cleaned).set_product_name().get_df()
        return self
    
    def order_columns(self):
        self.df_cleaned = BaseCleaner(self.df_cleaned).set_columns_order().get_df()
        return self

    def get_cleaned_df(self):
        return self.df_cleaned