from pathlib import Path
from string import Template
import sys

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))
    from velix.skills.ai_editor.models import EditorRequest
else:
    from .models import EditorRequest


class PromptBuilder:
    """
    Builds prompts for the AI editor.
    """

    def __init__(self, prompt_dir: Path | None = None):
        self.prompt_dir = prompt_dir or Path(__file__).parent / "prompts"

        self.system_prompt = (
            "You are an expert software engineer.\n"
            "You edit source code and configuration files.\n"
            "Return ONLY the modified file.\n"
            "Do not include explanations.\n"
            "Do not wrap the response inside markdown fences.\n"
        )

        self.rules = {
            "py": [
                "Return valid Python code.",
                "Preserve imports unless modification requires otherwise.",
                "Keep formatting clean.",
            ],
            "json": [
                "Return valid JSON.",
                "Do not add comments.",
                "Preserve existing meanings.",
            ],
            "md": [
                "Return valid Markdown.",
            ],
            "txt": [],
        }

    def build(self, request: EditorRequest) -> str:
        rules = self.rules.get(request.file_type, [])

        template = Template(
            """
$system

Task:
$instruction

Rules:
$rules

Current File:

$file
"""
        )

        return template.substitute(
            system=self.system_prompt,
            instruction=request.instruction,
            rules="\n".join(f"- {r}" for r in rules),
            file=request.original_content,
        )

    def add_rule(self, file_type: str, rule: str) -> None:
        self.rules.setdefault(file_type, []).append(rule)

    def set_system_prompt(self, prompt: str) -> None:
        self.system_prompt = prompt