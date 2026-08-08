from enum import Enum

class ParameterSource(Enum):
    NER = "ner"
    DEPENDENCY = "dependency"
    POS = "pos"
    REGEX = "regex"
    PHRASE = "phrase"
    ENTITY = "entity"
    ACTION = "action"
    TOKEN = "token"
    TEXT_SPAN = "text_span"
    RULE = "rule"
    CONTEXT = "context"
    USER = "user"
    SYSTEM = "system"