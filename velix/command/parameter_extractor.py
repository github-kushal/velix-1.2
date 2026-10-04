import os
import sys
from typing import Optional


sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.getcwd())
from dataclasses import dataclass, field

from nlp.semantic.entity_extractor import EntityMatch
from nlp.correction.spell_checker import SpellChecker
from nlp.NLPState import NLPState
from nlp.processor import Process
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

@dataclass
class Candidate:
    text: str

    sources: set[ParameterSource] = field(default_factory=set)

    ner_type: Optional[str] = None  # noqa: UP045
    entity_type: Optional[str] = None # noqa: UP045 

    parameter_type: Optional[ParameterType] = None # noqa: UP045
    action: Optional[str] = None # noqa: UP045
    role: Optional[ParameterRole] = None  # noqa: UP045
    canonical_name: Optional[str] = None # noqa: UP045

    confidence: float = 0.0
    is_valid: bool = True

    dependencies: list[tuple] = field(default_factory=list)

    start_token: Optional[int] = None # noqa: UP045
    end_token: Optional[int] = None # noqa: UP045

    

ROLE_RULES = {
            ParameterRole.TARGET: {
                ("OPEN", ParameterType.APPLICATION),
                ("OPEN", ParameterType.URL),
                ("OPEN", ParameterType.PATH),
            },

            ParameterRole.VALUE: {
                ("SET_VOLUME", ParameterType.NUMBER),
                ("SET_BRIGHTNESS", ParameterType.NUMBER),
            },

            ParameterRole.SOURCE: {
                ("MOVE", ParameterType.PATH),
                ("COPY", ParameterType.PATH),
            },
        }

SOURCE_WEIGHTS = {
    ParameterSource.NER: 0.85,
    ParameterSource.ENTITY: 0.90,
    ParameterSource.DEPENDENCY: 0.80,
    ParameterSource.REGEX: 0.95,
}

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


    def _get_action(self, candidate):
        for term in self.state.dependencies:
            text, dep, con = term  # noqa: RUF059

            if text.lower() == candidate.lower():  # noqa: SIM102
                if dep == "ROOT":  # noqa: RUF100, SIM102
                    return text
        return None


    def _get_parameter_roles(self, candidate, action) -> ParameterRole:
        for term in self.state.dependencies:
            text, dep, con = term

            if text.lower() == candidate.lower():  # noqa: SIM102
                if dep in ("dobj", "pobj", "obj"):  # noqa: RUF100, SIM102
                    if con == action or con == "on":
                        return ParameterRole.TARGET
                    if con == "for":
                        return ParameterRole.QUERY
                    else:
                        return ParameterRole.UNKNOWN


    def _get_strong_role(self, action, parameter_type):

        for role, rules in ROLE_RULES.items():
            if (action, parameter_type) in rules:
                return role
        # Is the UNKNOWN is inside the loop, after checking the very first rule it will check if the rule is matched or not. If not it will return UNKNOWN without checking the other rules.
        return ParameterRole.UNKNOWN


    def _assign_role(self, candidate, action, parameter_type):

        role = self._get_strong_role(action, parameter_type)

        if role != ParameterRole.UNKNOWN:
            return role

        role = self._get_parameter_roles(candidate, action)

        if role is not None or role != ParameterRole.UNKNOWN:
            return role

        return ParameterRole.UNKNOWN
    
    


    def _collect_candidates(self):
        candidates = {}

        def add_candidate(
            text,
            source,
            ner_type=None,
            entity_type=None,
            canonical_name=None,
            dependency=None,
            start_token=None,
            end_token=None
        ):
            key = text.strip().lower()

            if not key:
                return

            if key not in candidates:
                candidates[key] = Candidate(
                    text=text,
                    sources={source},
                    ner_type=ner_type,
                    entity_type=entity_type,
                    canonical_name=canonical_name,
                    dependencies=[],
                    start_token=start_token,
                    end_token=end_token
                )

            candidate = candidates[key]

            # Add another evidence source
            candidate.sources.add(source)

            # Preserve NER information
            if ner_type is not None:
                candidate.ner_type = ner_type

            # Preserve entity information
            if entity_type is not None:
                candidate.entity_type = entity_type

            if canonical_name is not None:
                candidate.canonical_name = canonical_name

            if start_token and end_token is not None:
                candidate.start_token = start_token
                candidate.end_token = end_token

            # Preserve dependency information
            if dependency is not None:
                candidate.dependencies.append(dependency)

        # -------------------------
        # NER candidates
        # -------------------------
        for entity in self._extract_ner_parameters() or []:
            text, label = entity

            add_candidate(
                text=text,
                source=ParameterSource.NER,
                ner_type=label
            )

        # -------------------------
        # Dependency candidates
        # -------------------------
        for dep in self._extract_dependency_parameters() or []:
            text, dep_label, connection = dep

            # Only dependency relations that can represent parameters
            if dep_label not in ("pobj", "obj", "dobj"):
                continue

            add_candidate(
                text=text,
                source=ParameterSource.DEPENDENCY,
                dependency=(dep_label, connection)
            )

        # -------------------------
        # Entity candidates
        # -------------------------
        for entity in self._extract_entity_parameters() or []:
            if isinstance(entity, EntityMatch):
                text = entity.matched_text
                entity_type = entity.entity_type
            else:
                text, entity_type = entity
            # print(f"\n\n Entity : {entity}")
            # text, entity_type = entity
            # print(f"\n\n Text : {text} \n Entity Type : {entity_type}")

            add_candidate(
                text=text,
                source=ParameterSource.ENTITY,
                entity_type=entity_type
            )

        # -------------------------
        # Regex candidates
        # -------------------------
        for match in self._extract_regex_parameters() or []:
            add_candidate(
                text=match,
                source=ParameterSource.REGEX
            )

        return list(candidates.values())

    def _process_candidates(self, candidates, action):
        for candidate in candidates:

            parameter_type = self._classify_parameters(candidate.text)

            assigned_role = self._assign_role(
                candidate.text,
                action,
                parameter_type
            )

            confidence = self._calculate_confidence(candidate)

            candidate.parameter_type = parameter_type
            candidate.action = action
            candidate.role = assigned_role
            candidate.confidence = confidence

        return candidates

    def _calculate_confidence(self, candidate):
        if not candidate.sources:
            return 0.0

        weights = [
            SOURCE_WEIGHTS.get(source, 0.0)
            for source in candidate.sources
        ]

        base_confidence = max(weights)

        agreement_bonus = (len(candidate.sources) - 1) * 0.05

        confidence = base_confidence + agreement_bonus

        return min(confidence, 1.0)

    


if __name__ == "__main__":
    # process = Process()

    # state = process.process("open chrome")
    # extr = ParameterExtractor(state)

    # # print("STATE ENTITIES:", extr.state.entities)
    # # print("ENTITY TYPE:", type(extr.state.entities))

    # # entities = extr._extract_entity_parameters()

    # # print("EXTRACTED ENTITIES:", entities)

    # # for entity in entities:
    # #     print("ITEM:", entity)
    # #     print("ITEM TYPE:", type(entity))

    # pro_can = extr._process_candidates(extr._collect_candidates(), extr._get_action(state.original_text))

    # print(
    #     f"\n\nGet Action: {extr._get_action('open chrome')}",
    #     "\n\nNER Parameters: ",extr._extract_ner_parameters(),
    #     "\n\nRegex Parameters: ", extr._extract_regex_parameters(),
    #     "\n\nDependency Parameters: ", extr._extract_dependency_parameters(),
    #     "\n\nEntity Parameters: ", extr._extract_entity_parameters(),
    #     "\n\nCollected Candidates: ", pro_can,
    #     "\n\nParameter type: ", extr._classify_parameters("microsoft"), "\n",
    #     f"\n Confidence: {extr._calculate_confidence(pro_can[0] if pro_can is not None and len(pro_can) > 0 else None):.2f}" 
    # )

    # # print(
    # #     "\n\n NER : ", extr._extract_ner_parameters(),
    # #     "\n\n Dependency : ", extr._extract_dependency_parameters(),
    # #     "\n\n Entity : ", extr._extract_entity_parameters(),
    # # )

    process = Process()

    tests = [
        "open chrome",
        "search for lo-fi music on youtube",
        "send an email to rahul",
        "set volume to 50",
    ]

    for text in tests:
        state = process.process(text)

        print("\nInput:", text)
        print("Action-related state:", state)