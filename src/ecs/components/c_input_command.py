from enum import Enum


class CInputCommand:
    def __init__(self, name: str, key:int) -> None:
        self.name = name
        self.key = key
        self.phase = CommandPhase.NONE

class CommandPhase(Enum):
    NONE = 0
    START = 1
    END = 2
