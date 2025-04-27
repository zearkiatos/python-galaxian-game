from enum import Enum

class CStateSpecial:
    def __init__(self, value: float, restrict_seconds: float) -> None:
        self.state = StateSpecial.IDLE
        self.value = value
        self.restrict_seconds = restrict_seconds
        self.start_time = 0.0

class StateSpecial(Enum):
    IDLE = 0
    ACTIVE = 1