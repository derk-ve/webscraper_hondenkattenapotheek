category_xpath = {
    "dierapotheker": {
        "product_element": "div[contains(@class, 'product') and contains(@class, 'box') and contains(@class, 'standard')]",
        "product_title": "a[contains(@class, 'name')]",
        "product_brand": "div[contains(@class, 'owner')]",
        "product_price_amount": "div[contains(@class, 'amount')]",
        "product_price_cents": "div[contains(@class, 'cent')]",
        "product_price_ex_sale": "span[contains(@class, 'list') and contains(@class, 'price')]",
        "product_delivery_info": "div[contains(@class, 'delivery') and contains(@class, 'information')]",
        "next_button": "label[contains(@for, 'next') and contains(@for, 'bottom')]"
    },
    "petmarkt": {
        "product_element": "div[contains(@class, 'product') and contains(@class, 'box')]",
        "product_title": "a[contains(@class, 'name')]",
        "product_price": "div[contains(@class, 'price')]",
        "product_delivery_info": "div[contains(@class, 'delivery') and contains(@class, 'information')]",
        "next_button": "label[contains(@for, 'next')]"
    },
    "hondenkattenapotheek": {
        "product_element": "div[contains(@class, 'product') and contains(@class, box) and contains(@class, 'mobile')]",
        "product_title": "div[contains(@class, 'name')]",
        "product_price": "span[contains(@class, 'price')]"
    }
}


product_xpath = {
    "dierapotheker": {
        "product_element": "div[contains(@class, 'product') and contains(@class, 'detail') and contains(@class, 'buy')]",
        "product_title": "div[contains(@class, 'name')]",
        "product_brand": "div[contains(@class, 'manufactur')]",
        "product_amount": "input[contains(@class, 'configur') and contains(@class, 'option')]",
        "product_main_price": "div[contains(@class, 'main') and contains(@class, 'price')]",
        "product_main_price_old": "div[contains(@class, 'old') and contains(@class, 'price')]",
        "product_price_container": "div[contains(@class, 'container') and contains(@class, 'price') and contains(@class, 'product')]",
        "product_price_row": "tr[contains(@class, 'price') and contains(@class, 'row')]",
        "product_savings_header": "th[contains(@class, 'saving')]"
    },
    "petmarkt": {
        "product_element": "div[contains(@class, 'product') and contains(@class, 'detail') and contains(@class, 'main')]",
        "product_title": "h1[contains(@class, 'name')]",
        "product_quantity_size_div": "div[contains(@class, 'product') and contains(@class, 'config') and contains(@class, 'group')]",
        "product_quantity_size_select": "select[contains(@class, 'product') and contains(@class, 'select') and contains(@class, 'config')]"
    },
    "medpets": {
        "product_element": "script[contains(text(), 'window.dataLayer.push')]",
        "product_title": "header",
        "product_quantity_size_div": "//div[contains(@class, 'mb-4')][.//button and .//ul]"
    },
    "pharmacy4pets": {
        "product_element": "div[contains(@class, 'product') and contains(@class, 'wrap')]",
        "product_title": "h1[contains(@class, 'title')]",
        "product_row_element": "tr[@class = 'row']"
    }
}
