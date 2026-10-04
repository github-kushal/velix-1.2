from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class NLPState:
    # ==========================
    # Raw Input
    # ==========================
    original_text: str

    # ==========================
    # Preprocessing
    # ==========================
    normalized_text: str = ""
    corrected_text: str = ""
    named_entities: dict[str, Any] = field(default_factory=dict)

    # ==========================
    # Token Processing
    # ==========================
    tokens: list[str] = field(default_factory=list)
    lemmas: list[str] = field(default_factory=list)
    filtered_tokens: list[str] = field(default_factory=list)
    expanded_tokens: list[str] = field(default_factory=list)

    # ==========================
    # Linguistic Analysis
    # ==========================
    pos_tags: list[str] = field(default_factory=list)
    dependencies: list[tuple] = field(default_factory=list)
 
    # ==========================
    # Intent & Entities
    # ==========================
    intent: Optional[str] = None
    intent_confidence: float = 0.0
    entities: dict[str, Any] = field(default_factory=dict)
    actions: list[tuple] = field(default_factory=list)

    # ==========================
    # Conversation Context
    # ==========================
    command_type: Optional[str] = None
    response_required: bool = True

    # ==========================
    # Metadata
    # ==========================
    metadata: dict[str, Any] = field(default_factory=dict)