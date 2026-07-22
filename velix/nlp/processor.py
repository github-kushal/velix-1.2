import spacy
# from spell_checker import SpellChecker
import os
from NLPState import NLPState
from preprocessing.normalizer import TextPreProcessor as tpp
from preprocessing.text_preprocessor import TextPreprocessor
from correction.spell_checker import SpellChecker
from parsing.dependency_parser import dependency_parser
from semantic.semantic_analyzer import SemanticAnalyzer



class Process:
    def __init__(self):
        """
        Purpose: value
        """
        
        self.nlp = spacy.load("en_core_web_trf")
        self.spell_checker = SpellChecker()
        self.semantic_analyzer = SemanticAnalyzer(self.nlp)
        self.pre_processor = TextPreprocessor(self.nlp)

    def process(self, user_input):
        """
        Purpose: process the text
        """
        state = NLPState(original_text=user_input)
        
        #------------------Normalize the user_input-----------------------

        norm_text = tpp(user_input)
        state.normalized_text = norm_text.preprocess()
        # print(type(state.normalized_text))
        # print(state.normalized_text)

        #------------------Spell Check-----------------------

        corrected_text = self.spell_checker.correct_sentence(state.normalized_text)
        state.corrected_text = corrected_text

        #------------------Pre-Processing phase-----------------------

        doc = self.nlp(state.corrected_text)

        preprocessed  = self.pre_processor.preprocess(doc)
        state.tokens = preprocessed.tokens
        state.lemmas = preprocessed.lemmas
        state.dependencies = dependency_parser(doc)

        #------------------Symantic Analysis----------------------

        analyse = self.semantic_analyzer.analyze(doc)
        print(analyse)

        return state
        
processor = Process()
processor.process("Open Chrome and search YouTube for Lo-fi music")