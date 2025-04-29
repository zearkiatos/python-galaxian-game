from enum import Enum
import pygame


class CHunterState:
    def __init__(self, start_position: pygame.Vector2) -> None:
        self.state = HunterState.IDLE
        self.start_position = pygame.Vector2(start_position.x, start_position.y)
    
class HunterState(Enum):
    IDLE = 0
    MOVE = 1
    RETURN = 2