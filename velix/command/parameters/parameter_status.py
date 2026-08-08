from enum import Enum

class ParameterStatus(Enum):
    CANDIDATE = "candidate"
    EXTRACTED = "extracted"
    NORMALIZED = "normalized"
    VALIDATED = "validated"
    AMBIGUOUS = "ambiguous"
    INVALID = "invalid"
    REJECTED = "rejected"
    RESOLVED = "resolved"