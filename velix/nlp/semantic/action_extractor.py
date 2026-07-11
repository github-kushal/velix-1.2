from phrase_extractor import PhraseExtractor as PE
import json


class ActionExtractor:
    def __init__(self):
        self.action_data = {}
        self.alias_map = {}
        self._load_action_data()
        self._build_alias_map()

    def _load_action_data(self):
        try:
            with open("data\\action_aliases.json", "r") as f:
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