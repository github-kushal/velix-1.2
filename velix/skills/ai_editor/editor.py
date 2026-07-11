from pathlib import Path
from time import perf_counter
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from velix.skills.ai_editor.file_manager import FileManager
    from velix.skills.ai_editor.prompt_builder import PromptBuilder
    from velix.skills.ai_editor.validator import Validator
    from velix.skills.ai_editor.llm_client import LLMClient
    from velix.skills.ai_editor.models import (
        EditorRequest,
        EditorResponse,
        ValidationResult,
    )
else:
    from .file_manager import FileManager
    from .prompt_builder import PromptBuilder
    from .validator import Validator
    from .llm_client import LLMClient
    from .models import (
        EditorRequest,
        EditorResponse,
        ValidationResult,
    )


class AIEditor:

    def __init__(self):

        self.file_manager = FileManager()
        self.prompt_builder = PromptBuilder()
        self.validator = Validator()
        self.llm = LLMClient()

    # ------------------------------------------------ #
    #                  PUBLIC API                      #
    # ------------------------------------------------ #

    def edit_file(
        self,
        file_path: Path,
        instruction: str,
    ) -> EditorResponse:

        start = perf_counter()

        try:

            request = self._build_request(
                file_path,
                instruction,
            )

            prompt = self._build_prompt(request)

            response = self._generate(prompt)

            validation = self._validate(
                response,
                request.file_type,
            )

            if not validation.is_valid:

                return self._failure(
                    "Validation failed.",
                    validation,
                    start,
                )

            self._save(
                file_path,
                response,
            )

            return self._success(
                response,
                validation,
                start,
            )

        except Exception as e:

            return self._failure(
                str(e),
                None,
                start,
            )

    # ------------------------------------------------ #
    #              PRIVATE METHODS                     #
    # ------------------------------------------------ #

    def _build_request(
        self,
        file_path: Path,
        instruction: str,
    ) -> EditorRequest:

        content = self.file_manager.read(file_path)

        return EditorRequest(
            file_path=file_path,
            instruction=instruction,
            original_content=content,
            file_type=self.file_manager.detect_file_type(file_path),
        )

    def _build_prompt(
        self,
        request: EditorRequest,
    ) -> str:

        return self.prompt_builder.build(request)

    def _generate(
        self,
        prompt: str,
    ) -> str:

        return self.llm.generate(prompt)

    def _validate(
        self,
        content: str,
        file_type: str,
    ) -> ValidationResult:

        return self.validator.validate(
            content,
            file_type,
        )

    def _save(
        self,
        file_path: Path,
        content: str,
    ) -> None:

        self.file_manager.write(
            file_path,
            content,
        )

    # ------------------------------------------------ #
    #            RESPONSE BUILDERS                     #
    # ------------------------------------------------ #

    def _success(
        self,
        content: str,
        validation: ValidationResult,
        start: float,
    ) -> EditorResponse:

        return EditorResponse(
            success=True,
            message="File edited successfully.",
            modified_content=content,
            validation=validation,
            execution_time=perf_counter() - start,
        )

    def _failure(
        self,
        message: str,
        validation: ValidationResult | None,
        start: float,
    ) -> EditorResponse:

        return EditorResponse(
            success=False,
            message=message,
            validation=validation,
            execution_time=perf_counter() - start,
        )

    # ------------------------------------------------ #
    #              Convenience API                     #
    # ------------------------------------------------ #

    def change_model(
        self,
        model: str,
    ):

        self.llm.change_model(model)

    def ping(self):

        return self.llm.ping()
    
if __name__ == "__main__":
    ae = AIEditor()
    response = ae.edit_file(
        file_path=Path("E:\\Velix-1.2\\velix\\nlp\\semantic\\data\\application_phrases.json"),
        instruction="""
Upgrade this JSON to the new semantic schema.

Requirements:
- Convert every phrase into an object.
- Include:
    canonical
    category
    priority
    description
- Preserve every existing phrase.
- Return only valid JSON.
""",
    )
    print(response)

    if response.success:
        print("Success!")
    else:
        print(response.message)