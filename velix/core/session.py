from dataclasses import dataclass
import time
import uuid
import secrets
from velix.nlp.nlp_matcher.NLPMatcher import *

@dataclass
class Commands:
    raw_text:str
    cleaned_text = raw_text.lower()
    intent : str
    entities : str
    timestamp = time.strftime("%H:%M:%S", time.localtime())
    status : str

class SessionManager:
    def __init__(self):
        """
        Purpose: 
        """
        self.current_command = None
        self.previous_command = None
        self.command_history = []
        self.session_start_time = datetime.now()
        self.command_count = 0
        self.session_id = None
        
    def start_session(self):
        self.session_id = str(uuid.uuid4())
        self.start_time = time.strftime("%H:%M:%S", time.localtime())
        self.command_count = 0
    
    def end_session(self):
        self.session_id = None
        self.start_time = None
        self.command_count = 0

    

        