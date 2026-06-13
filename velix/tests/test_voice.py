import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from voice import *  # or with aliases like you have

query = listener().lower()
speak(query)

