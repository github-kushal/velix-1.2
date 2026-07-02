from enum import Enum, auto
from dataclasses import dataclass

class States(Enum):
    BOOTING = auto()
    INITIALIZING = auto()
    AUTHENTICATING = auto()
    READY = auto()
    LISTENING = auto()
    PROCESSING = auto() 
    EXECUTING = auto()
    RESPONDING = auto()
    IDLE = auto()
    SLEEPING = auto()

@dataclass
class VoiceState:
    listening:bool = False
    speaking:bool = False
    transcribing:bool = False
    mic_ready:bool = False

@dataclass
class DeviceState:
    internet_available:bool = False
    microphone_connected: bool = False
    speaker_connected: bool = False

@dataclass
class ExecutionState:
    busy: bool = False
    processing: bool = False
    executing: bool = False


class StateManager:

    def __init__(self):
        """
        Purpose: 
        """
        self.voice = VoiceState()
        self.device = DeviceState()
        self.execution = ExecutionState()
        self.current_state = States.IDLE
        self.previous_state = States.BOOTING

    def set_state(self, new_state):
        self.previous_state = self.current_state
        self.current_state = new_state

    def get_state(self):
        return self.current_state

    def is_busy(self):
        return (
            self.execution.busy
            or self.execution.processing
            or self.execution.executing
        )

    
state = StateManager()
state.set_state(States.BOOTING)
print(state.get_state())
print(state.previous_state)