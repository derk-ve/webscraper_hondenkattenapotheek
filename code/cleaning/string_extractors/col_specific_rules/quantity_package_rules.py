import re
import pandas as pd
from ..string_extractor import StringExtractor
from ..string_extrac_rule import StringExtractRule


GENERAL_QUANTITY_CONTAINS_PATTERN = r"(\d{1,3})\s*(tabl|pip|stuks|cm)($|.*)"
GENERAL_QUANTITY_REPLACE_PATTERN = r"\1 \2"


class MilbemaxQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        if "kauwtabl" not in s:
            gen_result = self._apply_general_quantity_package_rule(s)

        else:
            return re.search(r"(\d+)\s*tabl", s).group(1) + " kauwtabl"

        if not pd.isna(gen_result):
            return gen_result

        elif "stuks" in s:
            return re.search(r"(\d{1,3})\s*stuks", s).group(1) + "tabl"

        elif re.search(r"4\s*\(2x2\)\s*tabl", s):
            return "4 tabl"

        print(f"Could not extract milbemax quantity_package from: {s}")
        return s


StringExtractor.register("milbemax_quantity_package", MilbemaxQuantityPackageExtractRule)


class AdvantixQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        print(f"Could not extract milbemax quantity_package from: {s}")
        return s


StringExtractor.register("advantix_quantity_package", AdvantixQuantityPackageExtractRule)


class DrontalQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        print(f"Could not extract drontal quantity_package from: {s}")
        return s


StringExtractor.register("drontal_quantity_package", DrontalQuantityPackageExtractRule)


class MilbactorQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        print(f"Could not extract milbactor quantity_package from: {s}")
        return s


StringExtractor.register("milbactor_quantity_package", MilbactorQuantityPackageExtractRule)


class MilproQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        elif "stuks" in s:
            return re.search(r"(\d{1,3})\s*stuks", s).group(1) + " tabl"

        elif "smakelijke tabl" in s:
            return re.search(r"(\d+) smakelijke tabl", s).group(1) + " tabl"

        print(f"Could not extract milpro quantity_package from: {s}")
        return s


StringExtractor.register("milpro_quantity_package", MilproQuantityPackageExtractRule)


class PanacurQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        elif re.search("250", s):
            return "10 tabl"

        elif re.search("500", s):
            return "10 tabl"

        elif self.matches_regex(r"(\d+)\s*(?:x\s*(\d+))?\s*injector", s):
            match = re.search(r"(\d+)\s*(?:x\s*(\d+))?\s*injector", s)

            if match.group(2):
                return f"{match.group(2)} injector"

            return match.group(1) + " injector"

        elif re.search(r"4[.,]8($|.*)", s):
            return "4,8 g ontwormpasta"

        print(f"Could not extract panacur quantity_package from: {s}")
        return s


StringExtractor.register("panacur_quantity_package", PanacurQuantityPackageExtractRule)


class SerestoQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        elif re.search(r"2\s*stuks", s) or re.search(r"(2|duo)\s*[-]\s*pack", s):
            return "2 pack"

        else:
            return "1 pack"


StringExtractor.register("seresto_quantity_package", SerestoQuantityPackageExtractRule)


class VectraQuantityPackageExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_package_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        print(f"Could not extract vectra quantity_package from: {s}")
        return s


StringExtractor.register("vectra_quantity_package", VectraQuantityPackageExtractRule)
