import spacy
# from spell_checker import SpellChecker
import os
from NLPState import NLPState
from normalizer import TextPreProcessor as tpp
from tokenizer import tokenizer
from lemmatizer import lemmatizer



class Process:
    def __init__(self):
        """
        Purpose: value
        """
        
        self.nlp = spacy.load("en_core_web_trf")
        # self.spell_checker = SpellChecker()

    def process(self, user_input):
        """
        Purpose: process the text
        """
        state = NLPState(original_text=user_input)
        
        #------------------Normalize the user_input-----------------------

        norm_text = tpp(user_input)
        state.normalized_text = norm_text.preprocess()

        #------------------Pre-Processing phase-----------------------

        doc = self.nlp(state.normalized_text)

        state.tokens = tokenizer(doc)
        state.lemmas = lemmatizer(doc)

        return state
        