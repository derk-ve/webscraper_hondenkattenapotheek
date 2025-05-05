import re
import pandas as pd
from ..string_extractor import StringExtractor
from ..string_extrac_rule import StringExtractRule


class MilbemaxSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if not pd.isna(animal) and "kat" in animal:

            if "klein" in s or "kitten" in s:
                return "S (< 2 kg)"

            else:
                return "L (> 2 kg)"

        if "klein" in s or re.search(r"0.*?5", s) or re.search(r"(^| )s($| )", s):
            return "S (0 - 5kg)"

        elif "groot" in s or re.search(r"5.*?25", s) or "grote" in s or re.search(r"(^| )m($| )", s):
            return "L (5 - 25kg)"

        print(f"Could not extract milbemax size from: {s}")
        return pd.NA


StringExtractor.register("milbemax_size", MilbemaxSizeExtractRule)


class AdvantixSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if re.search(r"(0|1[.,]5|<)\s*(-|tot)\s*4", s) or re.search(r"(tot|<)\s*4\s*kg", s):
            return "XS (1,5 - 4 kg)"

        elif re.search(r"4\s*(-|tot)\s*10", s):
            return "S (4 - 10 kg)"

        elif re.search(r"10\s*(-|tot)\s*25", s):
            return "M (10 - 25 kg)"

        elif re.search(r"25\s*(-|tot)\s*40", s):
            return "L (25 - 40 kg)"

        elif re.search(r"40\s*(-|tot)\s*60", s) or re.search(r"(>|≥)\s*40", s):
            return "XL (40 - 60 kg)"

        print(f"Could not extract advantix size from: {s}")
        return pd.NA


StringExtractor.register("advantix_size", AdvantixSizeExtractRule)


class DrontalSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if not pd.isna(animal) and "kat" in animal:

            if re.search(r"middel\s*grote", s):
                return "M (15mg - 60 mg)"

            elif "large" in s or "grote" in s or "groot" in s:
                return "L (24 - 96 mg)"

            return "S (7,5 - 30 mg)"

        if "large" in s or "groot" in s or "grote" in s or re.search(r"10.*?35", s):
            return "L (large dog)"

        elif "pup" in s:
            return "XS (pup)"

        return "S (small dog)"


StringExtractor.register("drontal_size", DrontalSizeExtractRule)


class MilbactorSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if not pd.isna(animal) and "kat" in animal:

            if "kleine" in s or "kitten" in s:
                return "S (4 - 10 mg)"

            elif "kat" in s:
                return "L (16 - 40 mg)"

        if re.search(r"25\s*-\s*50", s) or re.search(r">\s*5", s) or "grote" in s:
            return "L (25 - 250 mg)"

        elif re.search(r"0[,.]5\s*-\s*5", s) or re.search(r">\s*0[.,]5", s) or "klein" in s or "pup" in s:
            return "S (2.5 mg - 25.0 mg)"

        elif re.search(r"5\s*-\s*25", s) or re.search(r">\s*2[.,]5", s) or re.search(r"middel\s*(grote|groot)", s):
            return "M (12,5 mg - 125 mg)"

        print(f"Could not extract milbactor size from: {s}")
        return pd.NA


StringExtractor.register("milbactor_size", MilbactorSizeExtractRule)


class MilproSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if not pd.isna(animal) and "kat" in animal:

            if "klein" in s or "kitten" in s:
                return "S (< 2 kg)"

            else:
                return "L (> 2 kg)"

        if "klein" in s or "kleine" in s or re.search(r"0[.,]5\s*-\s*10", s):
            return "S (0,5 - 10 kg)"

        elif "grote" in s or "groot" in s or re.search(r"(≥|>)\s*5", s):
            return "L (> 5 kg)"

        print(f"Could not extract milpro size from: {s}")
        return pd.NA


StringExtractor.register("milpro_size", MilproSizeExtractRule)


class PanacurSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if "250" in s or "klein" in s:
            return "S (250 mg)"

        elif "500" in s or "grote" in s:
            return "L (500 mg)"

        elif "past" in s:
            return "M (petpaste)"

        print(f"Could not extract panacur size from: {s}")
        return pd.NA


StringExtractor.register("panacur_size", PanacurSizeExtractRule)


class SerestoSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if not pd.isna(animal) and "kat" in animal:
            return "M (38cm)"

        if re.search(r"(0|licht|<).*?8", s) or "klein" in s:
            return "S (< 8 kg)"

        elif re.search(r"8.*?meer", s) or re.search(r"(zwaar|>).*?8", s) or re.search(r'70\s*cm', s) or "groot" in s or "grote" in s:
            return "L (> 8 kg)"

        print(f"Could not extract seresto size from: {s}")
        return pd.NA


StringExtractor.register("seresto_size", SerestoSizeExtractRule)


class VectraSizeExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = str(s).lower()

        if "kat" in s:
            return "M (423 mg)"

        if re.search(r"(^| )xs( |$)", s) or re.search(r"1[.,]5\s*-\s*10", s):
            return "XS (1,5 - 4 kg)"

        elif re.search(r"(^| )s( |$)", s) or re.search(r"4\s*-\s*10", s):
            return "S (4 - 10 kg)"

        elif re.search(r"(^| )m( |$)", s) or re.search(r"10\s*-\s*25", s):
            return "M (10 - 25 kg)"

        elif re.search(r"(^| )l( |$)", s) or re.search(r"25\s*-\s*40", s):
            return "L (25 - 40 kg)"

        elif re.search(r"(^| )xl( |$)", s) or re.search(r"40\s*-\s*60", s) or re.search(r">\s*40", s):
            return "XL (40 - 60 kg)"

        print(f"Could not extract vectra size from: {s}")
        return pd.NA


StringExtractor.register("vectra_size", VectraSizeExtractRule)
