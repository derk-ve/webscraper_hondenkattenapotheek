from .base_prod_scraper import BaseProdScraper
from ...scraping.configs.xpath_configs import product_xpath
import pandas as pd
import re
from selenium.webdriver.common.by import By
import logging

logger = logging.getLogger(__name__)


class DierapothekerProdScraper(BaseProdScraper):

    def _scrape_product_page(self) -> dict:
        product = self.driver.find_element(By.XPATH, "//" + product_xpath[self.website]["product_element"])
        product_text = product.text
        product_text = self._clean_price_lines(product_text)

        product_lines = product_text.split("\n")
        bespaar = "bespaar" in product_text.lower()

        # Extract base price and sale price
        price_per_quantity, sale_price_per_quantity = self._extract_base_prices(product_text)

        # Extract tiered pricing per quantity
        quantity_price_rows = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_price_row"])
        for row in quantity_price_rows:
            if row.text.strip() and "Aantal" not in row.text:
                quantity, price, sale_price = self._parse_price_row(row.text, bespaar)
                if quantity:
                    price_per_quantity[quantity] = price
                    if sale_price is not None:
                        sale_price_per_quantity[quantity] = sale_price


        delivery_info = self._extract_delivery_info(product_lines)

        title = self._get_element_text(product, product_xpath["dierapotheker"]["product_title"])
        brand = self._get_element_text(product, product_xpath["dierapotheker"]["product_brand"])

        quantity_elements = product.find_elements(By.XPATH, ".//" + product_xpath["dierapotheker"]["product_amount"])
        quantity_options = [q.find_element(By.XPATH, "./ancestor::div[1]").text.strip() for q in quantity_elements]
        selected = [q.find_element(By.XPATH, "./ancestor::div[1]").text.strip() for q in quantity_elements if q.is_selected()]
        quantity = selected[0] if selected else title

        # Ensure both price dicts have the same keys
        all_quantities = set(price_per_quantity.keys()).union(set(sale_price_per_quantity.keys()))
        for qty in all_quantities:
            price_per_quantity.setdefault(qty, None)
            sale_price_per_quantity.setdefault(qty, None)

        return {
            "title": title,
            "brand": brand,
            "price": price_per_quantity,
            "sale_price": sale_price_per_quantity,
            "quantity_options": quantity_options,
            "quantity": quantity,
            "delivery_info": delivery_info
        }

    
    def _extract_base_prices(self, product_text: str):
        base_price_text = product_text.lower().split('aantal')[0]
        prices = re.findall(r"(\d+[.,]\d+)", base_price_text)
        logger.debug(f"Main Prices found: {prices}")
        # Convert prices to floats for comparison (handling both , and . as decimal separators)
        numeric_prices = [float(p.replace(",", ".")) for p in prices]

        if len(numeric_prices) < 2:
            # Not enough data to separate sale vs regular price
            return {"1": prices[0]} if prices else {}, {}

        # Determine which price is lower
        low, high = sorted(numeric_prices)
        sale_price = str(low).replace(".", ",")
        regular_price = str(high).replace(".", ",")
        return {"1": regular_price}, {"1": sale_price}

    def _parse_price_row(self, text: str, bespaar: bool) -> tuple[str, str, str]:
        clean_text = " ".join(text.split())
        quantity_match = re.search(r"((^| )\d+ )", clean_text)
        prices = re.findall(r"\d+[.,]\d+", clean_text)
        logger.debug(f"Row Prices: {prices}")

        if not quantity_match:
            return None, None, None

        quantity = quantity_match.group(1).strip()

        numeric_prices = [float(p.replace(",", ".")) for p in prices]
        sorted_prices = sorted(numeric_prices, reverse=True)  # Highest to lowest

        if len(sorted_prices) == 1:
            price = str(sorted_prices[0]).replace(".", ",")
            return quantity, price, None

        elif len(sorted_prices) == 2:
            if bespaar:
                price = str(sorted_prices[0]).replace(".", ",")
                sale_price = None
            else:
                price = str(sorted_prices[0]).replace(".", ",")
                sale_price = str(sorted_prices[1]).replace(".", ",")
            return quantity, price, sale_price

        elif len(sorted_prices) >= 3:
            price = str(sorted_prices[0]).replace(".", ",")
            sale_price = str(sorted_prices[1]).replace(".", ",")
            return quantity, price, sale_price

        return quantity, None, None
    
    def _clean_price_lines(self, text: str) -> str:
        """
        Joins price fragments like:
        €
        37,
        95
        into: €37,95
        """
        lines = text.splitlines()
        cleaned_lines = []
        i = 0

        while i < len(lines):
            line = lines[i].strip()
            if line == "€" and i + 2 < len(lines):
                # Look ahead for euro price fragments
                merged = f"€{lines[i+1].strip()}{lines[i+2].strip()}"
                cleaned_lines.append(merged)
                i += 3  # Skip next two lines
            else:
                cleaned_lines.append(line)
                i += 1

        return "\n".join(cleaned_lines)



    def _extract_delivery_info(self, lines: list[str]) -> str:
        return next((line for line in lines if "verz" in line and "grat" not in line), "")

    def _get_element_text(self, root, xpath: str) -> str:
        return root.find_element(By.XPATH, ".//" + xpath).text


