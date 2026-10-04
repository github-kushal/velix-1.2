import importlib.resources as imp_res
import json
import re
from datetime import datetime
from pathlib import Path

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
        # print(f"Protected words : \n\n{self.protected_words}\n\n")
        self._load_symspell_dictionaries()

    # ------------------------------------------------------------------
    # Public Methods
    # ------------------------------------------------------------------

    def correct_word(self, word: str) -> str:
        """
        Correct a single word using SymSpell.
        """

        try:

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

            suggestions = self.sym_spell.lookup(
                word,
                Verbosity.TOP,
                max_edit_distance=2
            )

            if suggestions:
                return suggestions[0].term

            return word

        except Exception as e:  # noqa: TRY203
            raise e  # noqa: TRY201

    def correct_sentence(self, sentence: str) -> str:
        """
        Correct an entire sentence.
        """

        try:
            # Split sentence into words
            tokens = sentence.split()

            corrected_tokens = [
                self.correct_word(token)
                for token in tokens
            ]

            return " ".join(corrected_tokens)

        except Exception as e:  # noqa: TRY203
            raise e  # noqa: TRY201

    # ------------------------------------------------------------------
    # Private Methods
    # ------------------------------------------------------------------

    def _load_custom_dictionary(
        self,
        dir_path: Path = Path("E:/Velix-1.2/velix/nlp/data/protected")
    ):
        """
        Loads all protected words from JSON files.
        """

        try:

            if not dir_path.exists():
                raise FileNotFoundError(
                    f"Protected dictionary folder not found: {dir_path}"
                )

            for file_path in dir_path.glob("*.json"):

                with open(file_path, "r", encoding="utf-8") as file:
                    data = json.load(file)

                self.protected_words.update(
                    word.lower()
                    for word in data
                )

        except Exception as e:  # noqa: TRY203
            raise e  # noqa: TRY201

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
                raise RuntimeError(
                    "Failed to load frequency dictionary."
                )

            if not self.sym_spell.load_bigram_dictionary(
                bigram_dict_path,
                term_index=0,
                count_index=2
            ):
                raise RuntimeError(
                    "Failed to load bigram dictionary."
                )

        except Exception as e:  # noqa: TRY203
            raise e  # noqa: TRY201

    # ------------------------------------------------------------------
    # Validation Methods
    # ------------------------------------------------------------------

    def _is_protected(self, word: str) -> bool:
        return bool(word.lower() in self.protected_words)

    def _word_exists(self, word: str) -> bool:
        return word.lower() in self.sym_spell.words

    def _is_number(self, word: str) -> bool:
        return bool(
            re.fullmatch(
                r"-?\d+(?:\.\d+)?",
                word.strip()
            )
        )

    def _is_url(self, word: str) -> bool:
        return bool(
            re.fullmatch(
                r"https?://\S+",
                word.strip(),
                re.IGNORECASE
            )
        )

    def _is_email(self, word: str) -> bool:
        return bool(
            re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                word.strip()
            )
        )

    def _is_file_path(self, word: str) -> bool:

        normalized = word.strip()

        if not normalized:
            return False

        has_separator = "/" in normalized or "\\" in normalized
        has_drive = bool(re.match(r"^[A-Za-z]:[\\/]", normalized))
        is_relative = normalized.startswith(
            ("./", ".\\", "../", "..\\")
        )
        has_extension = bool(
            re.search(r"\.[A-Za-z0-9]{1,10}$", normalized)
        )

        return (
            has_separator
            or has_drive
            or is_relative
            or has_extension
        )

    def _is_acronym(self, word: str) -> bool:
        return bool(
            re.fullmatch(
                r"[A-Z]{2,}",
                word.strip()
            )
        )

    def _is_date(self, value: str) -> bool:
        date_formats = [
            "%Y-%m-%d",   # 2026-08-12
            "%d/%m/%Y",   # 12/08/2026
            "%m/%d/%Y",   # 08/12/2026
            "%d-%m-%Y",   # 12-08-2026
            "%m-%d-%Y",   # 08-12-2026
        ]

        value = value.strip()

        for fmt in date_formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue

        return False


    def _is_time(self, value: str) -> bool:
        time_formats = [
            "%H:%M",       # 17:30
            "%H:%M:%S",    # 17:30:00
            "%I:%M %p",    # 5:30 PM
            "%I %p",       # 5 PM
        ]

        value = value.strip()

        for fmt in time_formats:
            try:
                datetime.strptime(value, fmt)
                return True
            except ValueError:
                continue

        return False