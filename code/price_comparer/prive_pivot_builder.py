import pandas as pd


class PricePivotBuilder:

    def __init__(self,
                 df: pd.DataFrame):

        self.df = df


    def build(self):

        base_columns = [
            "brand", "pet", "size",
            "quantity_package", "quantity_package_unit", "quantity_ordered"
        ]

        price_pivot = self.df.pivot_table(
            index=base_columns,
            columns="website",
            values="price",
            aggfunc="first"
        ).add_prefix("price_").reset_index()

        sale_price_pivot = self.df.pivot_table(
            index=base_columns,
            columns="website",
            values="sale_price",
            aggfunc="first"
        ).add_prefix("sale_price_").reset_index()

        url_pivot = self.df.pivot_table(
            index=base_columns,
            columns="website",
            values="product_link",
            aggfunc="first"
        ).add_prefix("url_").reset_index()

        title_pivot = self.df.pivot_table(
            index=base_columns,
            columns="website",
            values="title",
            aggfunc="first"
        ).add_prefix("title_").reset_index()

        result_df = pd.merge(price_pivot, sale_price_pivot, on=base_columns, how="outer")
        result_df = pd.merge(result_df, url_pivot, on=base_columns, how="outer")
        result_df = pd.merge(result_df, title_pivot, on=base_columns, how="outer")

        result_df = result_df.sort_values(
            by=[
                "brand", "pet", "size",
                "quantity_package", "quantity_ordered"
            ]
        ).reset_index()

        result_df = self._add_additional_info_columns(result_df)

        result_df = result_df[
            [
                "product_name", "brand", "pet", "size", "quantity_package", "quantity_package_unit", "quantity_ordered",
                "price_hondenkattenapotheek", "price_dierapotheker", "price_medpets", "price_petmarkt", "price_pharmacy4pets", "num_competitors",
                "avg_price", "diff_from_competitors", "is_cheapest", "spread_in_price",
                "title_hondenkattenapotheek", "title_dierapotheker", "title_medpets", "title_petmarkt", "title_pharmacy4pets",
                "url_dierapotheker", "url_medpets", "url_petmarkt", "url_pharmacy4pets",
                "is_owned_hondenkattenapotheek", "is_owned_dierapotheker", "is_owned_medpets", "is_owned_petmarkt", "is_owned_pharmacy4pets",
            ]
        ]

        return result_df


    def _add_additional_info_columns(self,
                                     result_df):

        competitor_cols = [
            "price_dierapotheker",
            "price_medpets",
            "price_petmarkt",
            "price_pharmacy4pets"
        ]

        result_df['product_name'] = result_df["pet"].astype(str) + "|" + result_df["brand"].astype(str) + "|" + result_df["size"].astype(str) + "|" + result_df["quantity_package"].astype(str) + " " + result_df["quantity_package_unit"].astype(str) 

        result_df["is_owned_hondenkattenapotheek"] = result_df["price_hondenkattenapotheek"].notna()
        result_df["is_owned_dierapotheker"] = result_df["price_dierapotheker"].notna()
        result_df["is_owned_medpets"] = result_df["price_medpets"].notna()
        result_df["is_owned_petmarkt"] = result_df["price_petmarkt"].notna()
        result_df["is_owned_pharmacy4pets"] = result_df["price_pharmacy4pets"].notna()

        result_df["avg_price"] = result_df[competitor_cols].mean(axis=1, skipna=True)

        result_df["diff_from_competitors"] = (
            result_df["price_hondenkattenapotheek"] - result_df["avg_price"]
        )

        result_df["is_cheapest"] = (
            result_df["price_hondenkattenapotheek"] <
            result_df[competitor_cols].min(axis=1, skipna=True)
        )

        result_df["spread_in_price"] = (
            result_df[competitor_cols].max(axis=1, skipna=True) -
            result_df[competitor_cols].min(axis=1, skipna=True)
        )

        result_df["num_competitors"] = result_df[competitor_cols].notna().sum(axis=1)

        return result_df


    def check_missing_prices(self,
                             result_df):

        def is_missing(row):

            website_col = f"price_{row['website']}"

            if website_col not in result_df.columns:
                print("returning true")
                return True

            subset = result_df[
                (result_df["brand"] == row["brand"]) &
                (result_df["size"] == row["size"]) &
                (result_df["quantity_package"] == row["quantity_package"])
            ]

            return row["price"] not in subset[website_col].values

        price_rows = self.df[self.df["price"].notna()].copy()

        missing_mask = price_rows.apply(is_missing, axis=1)

        return price_rows[missing_mask]


    
