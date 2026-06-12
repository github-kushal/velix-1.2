from enum import Enum

class States(Enum):
    BOOTING = 1
    INITIALIZING = 2
    AUTHENTICATING = 3
    READY = 4
    LISTENING = 5
    PROCESSING = 6 
    EXECUTING = 7
    RESPONDING = 8
    IDLE = 9
    SLEEPING = 10

states = list(States)
states = [s.name for s in states]
# print(states[1])

class StateManager():
    def current_state():
        