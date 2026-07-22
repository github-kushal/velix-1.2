from dataclasses import dataclass, field
from typing import List

from .phrase_extractor import PhraseExtractor
from .action_extractor import ActionExtractor
from .entity_extractor import EntityExtractor


@dataclass
class SemanticResult:
    text: str

    actions: list = field(default_factory=list)

    entities: list = field(default_factory=list)

    phrases: list = field(default_factory=list)

    confidence: float = 1.0


class SemanticAnalyzer:
    def __init__(self, nlp):
        self.nlp = nlp

        self.phrase_extractor = PhraseExtractor(nlp)
        self.action_extractor = ActionExtractor()
        self.entity_extractor = EntityExtractor(nlp)

    def analyze(self, doc) -> SemanticResult:
        """
        Complete semantic pipeline.

        Text
            ↓
        spaCy Doc
            ↓
        Phrase Extraction
            ↓
        Action Extraction
            ↓
        Entity Extraction
            ↓
        SemanticResult
        """

        

        # -----------------------------
        # Phrase Extraction
        # -----------------------------
        phrase_matches = self.phrase_extractor.extract(doc)
        # print("Phrase Matches:")
        # for p in phrase_matches:
        #     print(p)

        # -----------------------------
        # Action Extraction
        # -----------------------------
        # print("\nReceived phrase matches:")
        # print(phrase_matches)
        actions = self.action_extractor.extract(phrase_matches)

        # -----------------------------
        # Entity Extraction
        # -----------------------------
        entities = self.entity_extractor.extract(doc)

        # -----------------------------
        # Confidence
        # -----------------------------
        confidence = self._calculate_confidence(actions)

        # -----------------------------
        # Build Result
        # -----------------------------
        return SemanticResult(
            text=doc,
            actions=actions,
            entities=entities,
            phrases=phrase_matches,
            confidence=confidence,
        )

    def _calculate_confidence(self, actions):
        """
        Placeholder confidence calculation.

        Later this can use:
            - action confidence
            - phrase confidence
            - entity confidence
            - LLM verification
        """

        if not actions:
            return 0.0
        
        # print(type(actions))
        # print(actions)

        # for action in actions:
        #     print(type(action), action)

        return max(action.confidence for action in actions)