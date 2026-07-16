from action_extractor import ActionExtractor
from phrase_extractor import PhraseExtractor

class SemanticAnalyzer:
    def __init__(self, nlp):
        self.action_extractor = ActionExtractor()
        self.phrase_extractor = PhraseExtractor()