import pygame
class CHunter:
    def __init__(self, initial_position: pygame.Vector2) -> None:
        self.initial_position = initial_position
        self.chasing = False