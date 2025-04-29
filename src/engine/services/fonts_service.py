import pygame


class FontsService:
    DEFAULT_SIZE = 20
    def __init__(self)->None:
        self._fonts = {}

    def get(self, path: str, size: int = DEFAULT_SIZE) -> pygame.font:
        if path not in self._fonts:
            self._fonts[f"{path}_{size}"] = pygame.font.Font(path, size)
        return self._fonts[f"{path}_{size}"]