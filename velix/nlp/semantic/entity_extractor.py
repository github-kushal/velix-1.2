from dataclasses import dataclass
from pathlib import Path
import json
import os
from spacy.matcher import PhraseMatcher

@dataclass(frozen=True)
class EntityMatch:
    canonical_name : str

    entity_type : str

    matched_text : str

    start_token : int

    end_token : int

    # confidence : float

class EntityExtractor:
    def __init__(self, nlp):
        self.nlp = nlp
        self.entity_data = {}
        self.alias_map = {}
        self._load_entity_data()
        # print("\n", self.entity_data)
        self._build_alias_map()
        # print("\n",self.alias_map)
        self.matcher = self._build_matcher()
        self.extractors = [
            self._extract_domain_entities,
            self._extract_spacy_entities
        ]


    def _load_entity_data(self):
        try:
            for files in Path("E:\\Velix-1.2\\velix\\nlp\\semantic\\data\\").rglob("entity_data\\*.json"):
                # print("files : ",files)
                try:
                    with open(files, "r") as fl:
                        data = json.load(fl)
                        self.entity_data.update(data)
                    # return self.entity_data
                except Exception as e:
                    raise e
                except json.JSONDecodeError as e:
                    print(e)
                    # pass
                except (FileNotFoundError, OSError) as e:
                    print(f"File error: {e}")
                except TypeError as e:
                    print(f"Type error during JSON operation: {e}")
        except Exception as e:
            raise e
        except json.JSONDecodeError as e:
            return
        
    def _build_alias_map(self):
        try:
            for entity_id, entity_info in self.entity_data.items():
                for alias in entity_info["aliases"]:
                    self.alias_map[alias.lower()] = entity_id
            
        except Exception as e:
            raise e
        

    def _build_matcher(self):
        matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")
        
        for entity_key, info in self.entity_data.items():
            for alias in info["aliases"]:
                # print(f"alias : {alias}")
                pattern = self.nlp.make_doc(alias)
                matcher.add(info["id"], [pattern])
            # if info["id"] == "visual_studio_code":
            #     for alias in info["aliases"]:
            #         print(alias)
            
        # print(f"MATCHER : {len(matcher)}")
        return matcher


    def  _extract_spacy_entities(self, doc):
        return [(ent.text, ent.label_) for ent in doc.ents]

    def _extract_domain_entities(self, doc):
        matches = self.matcher(doc)
        # print(matches)

        result = []

        for match_id, start, end in matches:
            span = doc[start:end]
            entity_id = doc.vocab.strings[match_id]
            matched = EntityMatch(
                matched_text = span.text,
                entity_type = self.entity_data[entity_id]["entity_type"],
                canonical_name = self.entity_data[entity_id]["canonical"],
                start_token = start,
                end_token = end
            )
            # print("alias", self.entity_data[entity_id])

            result.append(matched)

        # print(result)
        return result
        

    def  _extract_regex_entities(self):
        pass

    def extract(self, doc):
        result = []

        for extractor in self.extractors:
            result.extend(extractor(doc))
            
        return result

if __name__ == "__main__":
    import spacy
    nlp = spacy.load("en_core_web_lg")
    doc = nlp("Open Visual Studio Code")
    print(doc)
    # ent = EntityExtractor(nlp)
    # print(ent.extract(doc))



