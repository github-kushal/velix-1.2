from datetime import datetime
import os
import sys

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.getcwd())
from dataclasses import dataclass

from nlp.correction.spell_checker import SpellChecker
from nlp.NLPState import NLPState
from parameters.parameter_roles import ParameterRole
from parameters.parameter_sources import ParameterSource
from parameters.parameter_status import ParameterStatus
from parameters.parameter_types import ParameterType


@dataclass
class ParameterMatch:
    value : str
    parameter_type : ParameterType
    role : ParameterRole
    source : ParameterSource
    start_token : int
    end_token : int
    confidence : float
    status : ParameterStatus

class ParameterExtractor:
    def __init__(self, state : NLPState):
        self.state = state
        self.spell_checker = SpellChecker()

    def _extract_ner_parameters(self):
        return self.state.named_entities

    def _extract_regex_parameters(self):
        pass

    def _extract_dependency_parameters(self):
        return self.state.dependencies

    def _extract_entity_parameters(self):
        return self.state.entities

    def _get_tokens(self):
        return self.state.tokens

    def _get_ner_parameter_type(self, candidate):
        for entity in self.state.named_entities:
            text, label = entity

            if text.lower() == candidate.lower():
                if label == "PERSON":
                    return ParameterType.PERSON

                elif label in ("GPE", "LOC"):
                    return ParameterType.LOCATION

                elif label == "ORG":
                    return ParameterType.ORGANIZATION

                elif label == "DATE":
                    return ParameterType.DATE

                elif label == "TIME":
                    return ParameterType.TIME

                elif label == "MONEY":
                    return ParameterType.AMOUNT

                elif label == "CARDINAL":
                    return ParameterType.NUMBER

        return None

    def _classify_parameters(self, candidate):
        ner_type = self._get_ner_parameter_type(candidate)
        
        if self.spell_checker._is_url(candidate):
            return ParameterType.URL
        elif self.spell_checker._is_email(candidate):
            return ParameterType.EMAIL
        elif self.spell_checker._is_number(candidate):
            return ParameterType.NUMBER
        elif self.spell_checker._is_file_path(candidate):
            return ParameterType.PATH
        elif self.spell_checker._is_date(candidate):
            return ParameterType.DATE
        elif self.spell_checker._is_time(candidate):
            return ParameterType.TIME
        elif ner_type is not None:
            return ner_type
        else:
            return ParameterType.TEXT

    def _assign_roles(self, candidate, action, parameter_type):
        pass


if __name__ == "__main__":
    ext = ParameterExtractor(NLPState(original_text="Search for 'How to bake cookies' on Google"))
    cls = ext._classify_parameters(NLPState(original_text="Search for 'How to bake cookies' on Google").original_text)
    print(cls)