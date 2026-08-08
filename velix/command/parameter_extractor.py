from dataclasses import dataclass

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

    def _extract_ner_parameters(self):
        return self.state.named_entities

    def _extract_regex_parameters(self):
        pass

    def _extract_dependency_parameters(self):
        return self.state.dependencies

    def _extract_entity_parameters(self):
        return self.state.entities

    def _classify_parameters(self, parameters):
        