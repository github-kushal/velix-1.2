import json
from dataclasses import dataclass

@dataclass
class ActionMatch:
    action: str
    matched_text: str
    priority : int
    confidence: float

class ActionExtractor:
    def __init__(self):

        self.action_data = {}
        self.alias_map = {}

        self._load_action_data()
        # print(self.action_data)
        self._build_alias_map()
        # print(self.alias_map)


    def _load_action_data(self):
        try:
            with open("E:\\Velix-1.2\\velix\\nlp\\semantic\\data\\action_data\\action_aliases.json", "r") as f:
                data = json.load(f)
                self.action_data.update(data)

        except Exception as e:
            raise e
        
    def _build_alias_map(self):
        try:
            for action, aliases in self.action_data.items():
                for alias in aliases["aliases"]:
                    self.alias_map[alias.lower()] = action
            
        except Exception as e:
            raise e
        
    def extract(self, phrase_matches):
        # print(f"\nMatches : {phrase_matches}\n")

        extracted_actions = []

        for phrase in phrase_matches:
            canonical = phrase["canonical"]
            # print("Canonical:", canonical)
            # print(type(canonical))
            # action = self.alias_map.get(canonical)
            # if action is None:
            #     continue
            # info = self.action_data[action]

            match = ActionMatch(
                action=canonical,
                matched_text=phrase["text"],
                priority=phrase["priority"],
                confidence=1.0
            )

            extracted_actions.append(match)
        
        return extracted_actions
       
        
if __name__ == "__main__":
    ae = ActionExtractor()
    print(ae.extract([{"canonical": "open", "text": "open chrome", "priority": 1}]))
