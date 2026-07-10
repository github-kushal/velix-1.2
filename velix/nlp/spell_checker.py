import os
import glob
import json
import importlib.resources as imp_res
import re
import math
from difflib import SequenceMatcher
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

        self.correct_word("opne")


    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def correct_word(self, word: str) -> str:
        """
        Correct a single word using SymSpell.
        """

        try:
            # Skip protected words and special tokens
            if (
                self._is_protected(word)
                or self._word_exists(word)
                or self._is_number(word)
                or self._is_url(word)
                or self._is_email(word)
                or self._is_file_path(word)
                or self._is_acronym(word)
            ):
                return word
            

            else:
                print(f"Words : {word}")
                suggestions = self.sym_spell.lookup(
                    word,
                    Verbosity.TOP,
                    max_edit_distance=2
                )


                best_suggestion = suggestions[0]
                # print(f"Suggestions : {best_suggestion}")

                if best_suggestion:
                    return best_suggestion.term

                # return word

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

    def _is_number(self, word: str) -> bool:
        """
        Returns True if the token is a numeric value.
        """

        return bool(re.fullmatch(r"-?\d+(?:\.\d+)?", word.strip()))

    def _is_url(self, word: str) -> bool:
        """
        Returns True if the token looks like a URL.
        """

        return bool(re.fullmatch(r"https?://\S+", word.strip(), re.IGNORECASE))

    def _is_email(self, word: str) -> bool:
        """
        Returns True if the token looks like an email address.
        """

        return bool(re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", word.strip()))

    def _is_file_path(self, word: str) -> bool:
        """
        Returns True if the token looks like a file path.
        """

        normalized = word.strip()

        if not normalized:
            return False

        has_separator = "/" in normalized or "\\" in normalized
        has_drive_prefix = bool(re.match(r"^[A-Za-z]:[\\/]", normalized))
        is_relative = normalized.startswith(("./", ".\\", "../", "..\\"))
        has_extension = bool(re.search(r"\.[A-Za-z0-9]{1,10}$", normalized))

        return has_separator or has_drive_prefix or is_relative or has_extension

    def _is_acronym(self, word: str) -> bool:
        """
        Returns True if the token is an uppercase acronym.
        """

        return bool(re.fullmatch(r"[A-Z]{2,}", word.strip()))
    
    

SpellChecker()