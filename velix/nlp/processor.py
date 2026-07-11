import spacy
# from spell_checker import SpellChecker
import os
from NLPState import NLPState
from velix.nlp.preprocessing.normalizer import TextPreProcessor as tpp
from velix.nlp.preprocessing.tokenizer import tokenizer
from velix.nlp.preprocessing.lemmatizer import lemmatizer
from velix.nlp.preprocessing.lemmatizer import pos_tagger
from velix.nlp.preprocessing.lemmatizer import ner
from velix.nlp.correction.spell_checker import SpellChecker
from velix.nlp.parsing.dependency_parser import dependency_parser



class Process:
    def __init__(self):
        """
        Purpose: value
        """
        
        self.nlp = spacy.load("en_core_web_trf")
        self.spell_checker = SpellChecker()

    def process(self, user_input):
        """
        Purpose: process the text
        """
        state = NLPState(original_text=user_input)
        
        #------------------Normalize the user_input-----------------------

        norm_text = tpp(user_input)
        state.normalized_text = norm_text.preprocess()

        #------------------Spell Check-----------------------

        corrected_text = self.spell_checker.correct_sentence(state.normalized_text)
        state.corrected_text = corrected_text

        #------------------Pre-Processing phase-----------------------

        doc = self.nlp(state.corrected_text)

        state.tokens = tokenizer(doc)
        state.lemmas = lemmatizer(doc)
        state.pos_tags = pos_tagger(doc)
        state.entities = ner(doc)
        state.dependencies = dependency_parser(doc)

        return state
        