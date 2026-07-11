import json
import os
from glob import glob
from spacy.matcher import Matcher

class PhraseExtractor:
    def __init__(self, nlp):
        self.phrase_dict = {}
        self._load_patterns()
        self.matcher = self._build_matcher(nlp)
        print(self.phrase_dict)

    def _load_patterns(self):
        try:
            for file in glob(os.path.join("E:\\Velix-1.2\\velix\\nlp\\semantic\\data", "*.json")):
                with open(file, "r") as f:
                    data = json.load(f)
                    self.phrase_dict.update(data)
                # print(f"data: {data}")
            return self.phrase_dict
        except Exception as e:
            raise e
    def _build_matcher(self, nlp):
        matcher = Matcher(nlp.vocab)
        for phrase, patterns in self.phrase_dict.items():
            matcher.add(phrase, [patterns])

        return matcher
    
    def extract(self, doc):
        
        matches = self.matcher(doc)
        
        for match_id, start, end in matches:
            span = doc[start:end]
            matched = {
                "text": span.text,
                "canonical": self.phrase_dict[doc.vocab.strings[match_id]],
                "start": start,
                "end": end
            } 
        
        yield matched

PhraseExtractor()