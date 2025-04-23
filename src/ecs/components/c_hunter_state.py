from enum import Enum


class CHunterState:
    def __init__(self) -> None:
        self.state = HunterState.IDLE
    
class HunterState(Enum):
    IDLE = 0
    MOVE = 1