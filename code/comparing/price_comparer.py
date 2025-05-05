import pandas as pd


class PriceComparer:

    def __init__(self,
                 old_file_path,
                 new_file_path):

        self.old_file_path = old_file_path
        self.new_file_path = new_file_path
        self.df_old = pd.DataFrame()
        self.df_new = pd.DataFrame()
        self.key_cols = [
            "product_name", "pet", "brand", "size", "quantity_package",
            "quantity_package_unit", "quantity_ordered"
        ]


    def load_data(self):

        self.df_old = pd.read_excel(self.old_file_path)
        self.df_new = pd.read_excel(self.new_file_path)

        self.df_old.set_index(self.key_cols, inplace=True)
        self.df_new.set_index(self.key_cols, inplace=True)


    def get_diff(self):

        price_cols = [col for col in self.df_old.columns if col.startswith("price")]
        is_owned_cols = [col for col in self.df_old.columns if col.startswith("is_owned")]
        other_cols = [
            "num_competitors", "avg_price",
            "diff_from_competitors", "is_cheapest"
        ]

        common_index = self.df_old.index.intersection(self.df_new.index)

        old_filtered = self.df_old.loc[common_index, price_cols + is_owned_cols + other_cols]
        new_filtered = self.df_new.loc[common_index, price_cols + is_owned_cols + other_cols]

        diff = old_filtered.compare(new_filtered, keep_shape=False, keep_equal=False)
        diff.columns = [
            f"{col[0]}_{'old' if col[1] == 'self' else 'new'}"
            for col in diff.columns
        ]

        for base_col in set(c.rsplit("_", 1)[0] for c in diff.columns):
            old_col = f"{base_col}_old"
            new_col = f"{base_col}_new"

            if old_col in diff.columns and new_col in diff.columns:

                mask = pd.isna(diff[old_col]) | pd.isna(diff[new_col])
                diff.loc[mask, [old_col, new_col]] = pd.NA

        diff.dropna(how="all", inplace=True)

        return diff.reset_index()


    def get_new_rows(self):

        new_rows = self.df_new.loc[~self.df_new.index.isin(self.df_old.index)]

        return new_rows.reset_index()


    def get_removed_rows(self):

        removed_rows = self.df_old.loc[~self.df_old.index.isin(self.df_new.index)]

        return removed_rows.reset_index()


    def run(self):

        self.load_data()

        diff = self.get_diff()
        new_rows = self.get_new_rows()
        removed_rows = self.get_removed_rows()

        return diff, new_rows, removed_rows

