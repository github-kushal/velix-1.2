import ast
import json
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from velix.skills.ai_editor.models import ValidationResult
else:
    from .models import ValidationResult


class Validator:

    def validate(self, content: str, file_type: str) -> ValidationResult:

        validators = {
            "json": self._validate_json,
            "py": self._validate_python,
            "txt": self._validate_text,
            "md": self._validate_text,
            "yaml": self._validate_text,
            "yml": self._validate_text,
        }

        validator = validators.get(file_type, self._validate_unknown)

        return validator(content)


    # ---------------- JSON ---------------- #

    def _validate_json(self, content: str) -> ValidationResult:

        try:
            json.loads(content)

            return ValidationResult(
                is_valid=True,
                file_type="json"
            )

        except json.JSONDecodeError as e:

            return ValidationResult(
                is_valid=False,
                file_type="json",
                errors=[str(e)]
            )


    # ---------------- Python ---------------- #

    def _validate_python(self, content: str) -> ValidationResult:

        try:
            ast.parse(content)

            return ValidationResult(
                is_valid=True,
                file_type="py"
            )

        except SyntaxError as e:

            return ValidationResult(
                is_valid=False,
                file_type="py",
                errors=[str(e)]
            )


    # ---------------- Plain Text ---------------- #

    def _validate_text(self, content: str) -> ValidationResult:

        return ValidationResult(
            is_valid=True,
            file_type="text"
        )


    # ---------------- Unknown ---------------- #

    def _validate_unknown(self, content: str) -> ValidationResult:

        return ValidationResult(
            is_valid=True,
            file_type="unknown",
            warnings=["No validator available."]
        )