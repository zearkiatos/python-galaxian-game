from enum import Enum
class CTagText:
    def __init__(self, value: str)->None:
        self.value = value
        self.state = TextState.IDLE

class TextState(Enum):
    IDLE = 0
    ACTIVE = 1