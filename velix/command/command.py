from dataclasses import dataclass
from datetime import time

@dataclass
class Command:
    action : str
    target : str
    parameters : dict
    priority : int
    confidence : float