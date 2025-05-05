from abc import ABC, abstractmethod
import re
import pandas as pd


GENERAL_QUANTITY_PACKAGE_CONTAINS_PATTERN = r"(\d{1,3})\s*(?:\(\d+\))?\s*(tabl|pip|ml)($|.*)"
GENERAL_QUANTITY_ORDERED_CONTAINS_PATTERN = r"(\d{1,2})\s*x\s*\d{1,3}"


class StringExtractRule(ABC):

    @abstractmethod
    def apply(self,
              s: str):
        
        pass


    def lower_string(self,
                     s: str) -> str:

        return s.lower()


    def matches_regex(self,
                      pattern: str,
                      s: str) -> bool:

        return bool(re.search(pattern, s))


    def _apply_general_quantity_package_rule(self,
                                             s: str) -> str:

        if self.matches_regex(GENERAL_QUANTITY_PACKAGE_CONTAINS_PATTERN, s):
            return re.search(GENERAL_QUANTITY_PACKAGE_CONTAINS_PATTERN, s).group(1) + " " + re.search(GENERAL_QUANTITY_PACKAGE_CONTAINS_PATTERN, s).group(2)
        return pd.NA


    def _apply_general_quantity_ordered_rule(self,
                                             s: str) -> str:

        if self.matches_regex(GENERAL_QUANTITY_ORDERED_CONTAINS_PATTERN, s):
            return int(re.search(GENERAL_QUANTITY_ORDERED_CONTAINS_PATTERN, s).group(1))
        return pd.NA
