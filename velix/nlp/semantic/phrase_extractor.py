import json
import os
from glob import glob
from spacy.matcher import Matcher
from pathlib import Path

class PhraseExtractor:
    def __init__(self, nlp):
        self.phrase_dict = {}
        self._load_patterns()
        # print(self.phrase_dict)
        # self._build_matcher(nlp)
        self.matcher = self._build_matcher(nlp)

    def _load_patterns(self):
        try:
            for files in Path("E:\\Velix-1.2\\velix\\nlp\\semantic\\data\\").rglob("phrase_data\\*.json"):
                with open(files, "r", encoding="utf-8") as file:
                    data = json.load(file)

                    for phrase, info in data.items():
                        self.phrase_dict[phrase] = info
                 
                    # for phrase_n_info in data:

                    
                # print(type(data))
                # print(f"data: {data}")
            # return self.phrase_dict
        except TypeError as e:
            raise TypeError(f"Error loading patterns: {e}")
        
        except Exception as e:
            raise e
        
        except AttributeError as e:
            raise AttributeError(f"Error loading patterns: {e}")
        
        except ValueError as e:
            raise ValueError(f"Error loading patterns: {e}")
        
    def _build_matcher(self, nlp):
        try:
            matcher = Matcher(nlp.vocab)
            for phrase, info in self.phrase_dict.items():
                # print(phrase, [patterns])
                matcher.add(phrase, [info["pattern"]])
            # print(matcher)

            # matcher.add(
            #     "TEST",
            #     [[
            #         {"LOWER": "open"},
            #         {"LOWER": "browser"}
            #     ]]
            # )

            # doc = nlp("open browser")

            # print(matcher(doc))
            return matcher
        except Exception as e:
            raise e
    
    def extract(self, doc):
        
        matches = self.matcher(doc)
        # print("mathces: ",matches)

        result = []
        
        for match_id, start, end in matches:
            # print("loop started")
            span = doc[start:end]
            phrase_id = doc.vocab.strings[match_id]
            # print(f"\ninfo : {self.phrase_dict[phrase_id]}\n")
            matched = {
                "text": span.text,
                "canonical": self.phrase_dict[phrase_id]["canonical"],
                "action" : self.phrase_dict[phrase_id]["action"],
                "category" : self.phrase_dict[phrase_id]["category"],
                "description": self.phrase_dict[phrase_id]["description"],
                "pattern" : self.phrase_dict[phrase_id]["pattern"],
                "priority" : self.phrase_dict[phrase_id]["priority"],
                "start": start,
                "end": end
            }
            # print(span)
        
            result.append(matched)
        # print(result)
        return result

if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_trf")
    doc = nlp("create folder")
    # for tok in doc:
    #     print(f"Tokens : {tok.text}, lower : {tok.lower_}")
    pe = PhraseExtractor(nlp)
    print(pe.extract(doc))
    