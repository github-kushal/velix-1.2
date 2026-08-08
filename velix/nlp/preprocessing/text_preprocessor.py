"""
text_preprocessor.py

Handles all preprocessing before semantic analysis.
"""

from dataclasses import dataclass


from .tokenizer import tokenizer
from .lemmatizer import lemmatizer
from .pos_tagger import pos_tagger
from .ner import ner


@dataclass
class PreprocessedText:

    doc: object

    tokens: list[str]

    lemmas: list[str]

    pos_tags: list

    named_entities: list


class TextPreprocessor:

    def __init__(self, nlp):
        self.nlp = nlp

    def preprocess(self, doc) -> PreprocessedText:
        """
        Complete preprocessing pipeline.

        Raw Text
            ↓
        (Spell correction - later)
            ↓
        spaCy Doc
            ↓
        Tokenizer
            ↓
        Lemmatizer
            ↓
        POS Tagger
            ↓
        NER
        """

        # Later replace with spell corrector
        

        tokens = tokenizer(doc)

        lemmas = lemmatizer(doc)

        pos = pos_tagger(doc)

        entities = ner(doc)

        return PreprocessedText(
            doc=doc,
            tokens=tokens,
            lemmas=lemmas,
            pos_tags=pos,
            named_entities=entities
        )