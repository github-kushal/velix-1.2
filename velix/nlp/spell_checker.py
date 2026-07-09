import os
import glob
import json
import importlib.resources as imp_res

from symspellpy import SymSpell, Verbosity


class SpellChecker:
    def __init__(self):
        """
        Initializes the spell checker and loads all required resources.
        """

        self.protected_words = set()
        self.sym_spell = SymSpell(
            max_dictionary_edit_distance=2,
            prefix_length=7
        )

        self._load_custom_dictionary()
        self._load_symspell_dictionaries()

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def correct_word(self, word: str) -> str:
        """
        Correct a single word using SymSpell.
        """

        try:
            # Skip protected words
            if self._is_protected(word):
                return word

            # Skip correctly spelled words
            if self._word_exists(word):
                return word

            suggestions = self.sym_spell.lookup(
                word,
                Verbosity.CLOSEST,
                max_edit_distance=2
            )

            if suggestions:
                # Return the best suggestion
                return suggestions[0].term

            return word

        except Exception as e:
            raise e

    def correct_sentence(self, tokens: list[str]) -> str:
        """
        Correct every token in a sentence.
        """

        try:
            corrected_tokens = [
                self.correct_word(token)
                for token in tokens
            ]

            return " ".join(corrected_tokens)

        except Exception as e:
            raise e

    # ------------------------------------------------------------------
    # Private Methods
    # ------------------------------------------------------------------

    def _load_custom_dictionary(self, dir_path: str = "data\\protected"):
        """
        Loads all protected words from JSON files.
        """

        try:
            if not os.path.exists(dir_path):
                raise FileNotFoundError(
                    f"Protected dictionary folder not found: {dir_path}"
                )

            files_path = glob.glob(os.path.join(dir_path, "*.json"))

            for file_path in files_path:
                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                    self.protected_words.update(
                        word.lower()
                        for word in data
                    )

        except Exception as e:
            raise e

    def _load_symspell_dictionaries(self):
        """
        Loads SymSpell frequency dictionaries.
        """

        try:
            dict_path = (
                imp_res.files("symspellpy")
                / "frequency_dictionary_en_82_765.txt"
            )

            bigram_dict_path = (
                imp_res.files("symspellpy")
                / "frequency_bigramdictionary_en_243_342.txt"
            )

            if not self.sym_spell.load_dictionary(
                dict_path,
                term_index=0,
                count_index=1
            ):
                raise RuntimeError("Failed to load frequency dictionary.")

            if not self.sym_spell.load_bigram_dictionary(
                bigram_dict_path,
                term_index=0,
                count_index=2
            ):
                raise RuntimeError("Failed to load bigram dictionary.")

        except Exception as e:
            raise e

    def _is_protected(self, word: str) -> bool:
        """
        Returns True if the word should never be corrected.
        """

        return word.lower() in self.protected_words

    def _word_exists(self, word: str) -> bool:
        """
        Returns True if the word exists in the SymSpell dictionary.
        """

        return word.lower() in self.sym_spell.words