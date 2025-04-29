from enum import Enum

class CStateSpecial:
    def __init__(self, value: float, restrict_seconds: float, duration_time: float = 0.0) -> None:
        self.state = StateSpecial.IDLE
        self.value = value
        self.restrict_seconds = restrict_seconds
        self.start_time = 0.0
        self.duration_time = duration_time

class StateSpecial(Enum):
    NONE = -1
    IDLE = 0
    ACTIVE = 1