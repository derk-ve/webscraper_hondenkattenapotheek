import re
import pandas as pd
from ..string_extractor import StringExtractor
from ..string_extrac_rule import StringExtractRule


class MilbemaxQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        else:
            return 1


StringExtractor.register("milbemax_quantity_ordered", MilbemaxQuantityOrderedExtractRule)


class AdvantixQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        else:
            return 1


StringExtractor.register("advantix_quantity_ordered", AdvantixQuantityOrderedExtractRule)


class DrontalQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        else:
            return 1


StringExtractor.register("drontal_quantity_ordered", DrontalQuantityOrderedExtractRule)


class MilbactorQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        else:
            return 1


StringExtractor.register("milbactor_quantity_ordered", MilbactorQuantityOrderedExtractRule)


class MilproQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        else:
            return 1


StringExtractor.register("milpro_quantity_ordered", MilproQuantityOrderedExtractRule)


class PanacurQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        else:
            return 1


StringExtractor.register("panacur_quantity_ordered", PanacurQuantityOrderedExtractRule)


class SerestoQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result

        elif re.search(r"4\s*x\s*gr", s):
            return 4
        
        else:
            return 1


StringExtractor.register("seresto_quantity_ordered", SerestoQuantityOrderedExtractRule)


class VectraQuantityOrderedExtractRule(StringExtractRule):

    def apply(self,
              s: str,
              animal=None):

        s = self.lower_string(s)

        gen_result = self._apply_general_quantity_ordered_rule(s)

        if not pd.isna(gen_result):
            return gen_result
        
        else:
            return 1


StringExtractor.register("vectra_quantity_ordered", VectraQuantityOrderedExtractRule)
