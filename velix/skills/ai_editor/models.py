from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, List
from datetime import datetime


# ---------- Backup ----------

@dataclass(slots=True)
class BackupInfo:
    original_path: Path
    backup_path: Path
    created_at: datetime
    size: int


# ---------- Validation ----------

@dataclass(slots=True)
class ValidationResult:
    is_valid: bool
    file_type: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


# ---------- Request ----------

@dataclass(slots=True)
class EditorRequest:
    file_path: Path
    instruction: str
    original_content: str
    file_type: str
    create_backup: bool = True
    overwrite: bool = True


# ---------- Response ----------

@dataclass(slots=True)
class EditorResponse:
    success: bool
    message: str
    modified_content: Optional[str] = None
    backup_info: Optional[BackupInfo] = None
    validation: Optional[ValidationResult] = None
    execution_time: float = 0.0