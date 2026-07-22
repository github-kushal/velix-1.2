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
        
        print("hello world")

        start = perf_counter()

        try:

            request = self._build_request(
                file_path,
                instruction,
            )

            prompt = self._build_prompt(request)

            response = self._generate(prompt)

            print(f"Response : {response}")

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
    


ENTITY_FILES = [
    "communication_phrases.json",
    "file_phrases.json",
    "media_phrases.json",
    "phrasal_verbs.json",
    "reminder_phrases.json",
    "search_phrases.json",
    "system_phrases.json",
    "utility_phrases.json",
    "web_phrases.json"
]


# with open("E:\\Velix-1.2\\velix\\nlp\\semantic\\data\\entity_data\\prompt.txt", "r") as data:
#     prompt = data.read()
# print(PROMPT)




ai = AIEditor()

entity_root = Path("E:/Velix-1.2/velix/nlp/semantic/data/phrase_data")


for filename in ENTITY_FILES:

    file_path = Path(entity_root / filename)
    print(f"\nFilepath : {file_path}")

    print(f"Processing {filename}")

    category_path = file_path.stem

    print(f"category : {category_path}")

    response = ai.edit_file(
        Path(file_path), 
        instruction=f"""
            You are updating the phrase data for the VELIX NLP semantic layer.

            ### Objective

            Update every phrase entry by adding a new field named `"action"`.

            The `"action"` field must contain the normalized high-level action that corresponds to the phrase.

            Example:

            ```json
            {{
                "open browser": {{
                    "canonical": "OPEN_BROWSER",
                    "action": "OPEN",
                    "category": "Browser Actions",
                    "priority": 1,
                    "description": "Open the default browser",
                    "pattern": [
                        {{"LOWER": "open"}},
                        {{"LOWER": "browser"}}
                    ]
                }}
            }}
            ```

            ---

            ### Action Mapping Rules

            Determine the action from the command meaning, not from the canonical name alone.

            Examples:

            * OPEN_BROWSER → OPEN
            * OPEN_APPLICATION → OPEN
            * CLOSE_BROWSER → CLOSE
            * CLOSE_WINDOW → CLOSE
            * SEARCH_GOOGLE → SEARCH
            * SEARCH_YOUTUBE → SEARCH
            * SEARCH_ONLINE → SEARCH
            * CREATE_FOLDER → CREATE
            * CREATE_FILE → CREATE
            * DELETE_FILE → DELETE
            * DELETE_FOLDER → DELETE
            * RENAME_FILE → RENAME
            * RENAME_FOLDER → RENAME
            * DOWNLOAD_FILE → DOWNLOAD
            * UPLOAD_FILE → UPLOAD
            * SEND_EMAIL → SEND
            * SEND_MESSAGE → SEND
            * REPLY_MESSAGE → REPLY
            * MAKE_CALL → CALL
            * ANSWER_CALL → ANSWER
            * REJECT_CALL → REJECT
            * PLAY_MUSIC → PLAY
            * PAUSE_MUSIC → PAUSE
            * STOP_MUSIC → STOP
            * RESUME_MUSIC → RESUME
            * NEXT_SONG → NEXT
            * PREVIOUS_SONG → PREVIOUS
            * SET_REMINDER → SET
            * REMOVE_REMINDER → REMOVE
            * SHOW_CALENDAR → SHOW
            * SHOW_WEATHER → SHOW
            * CHECK_WEATHER → CHECK
            * RESTART_COMPUTER → RESTART
            * SHUTDOWN_COMPUTER → SHUTDOWN
            * LOCK_COMPUTER → LOCK
            * LOG_OFF → LOG_OUT
            * TURN_ON_WIFI → TURN_ON
            * TURN_OFF_WIFI → TURN_OFF
            * ENABLE_BLUETOOTH → ENABLE
            * DISABLE_BLUETOOTH → DISABLE

            For any phrase not listed above, infer the most appropriate high-level action from its intent.

            ---

            ### Requirements

            * Update **every phrase entry**.
            * Preserve every existing field.
            * Only insert the new `"action"` field.
            * Do not modify:

            * canonical
            * category
            * priority
            * description
            * pattern
            * Keep formatting and indentation identical.
            * Do not rename keys.
            * Do not reorder entries.
            * Ensure the resulting JSON is valid.
            * After updating, validate the JSON for syntax errors and automatically fix any formatting issues before saving.
            * The output should overwrite the existing file.


            """
        )
    
    with open("response.txt", "a", encoding="utf-8") as output:
        output.write(f"{filename}\n{response}")
    

    if response.success:
        print("Success")
    else:
        print(response.message)








        