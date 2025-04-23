import pandas as pd


class StringExtractor:
    _registry = {}

    @classmethod
    def register(cls,
                 brand: str,
                 extrac_rule_cls):

        cls._registry[brand.lower()] = extrac_rule_cls()


    @classmethod
    def get(cls,
            brand: str):

        return cls._registry.get(brand.lower())


    @classmethod
    def extract(cls,
                brand: str,
                s_to_extract: str,
                animal: str):

        extract_rule = cls.get(brand)
        if extract_rule:
            return extract_rule.apply(s_to_extract, animal)

        print(f"No extractor registered for brand: {brand}")
        return pd.NA

