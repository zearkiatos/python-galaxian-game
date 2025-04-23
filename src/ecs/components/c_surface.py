import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.Color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)
        self.area = self.surface.get_rect()

    @classmethod
    def from_surface(cls, surface: pygame.Surface) -> "CSurface":
        c_surface = cls(pygame.Vector2(0,0), pygame.Color(0, 0, 0))
        c_surface.surface = surface
        c_surface.area = surface.get_rect()
        return c_surface

    def get_area_relative(area: pygame.Rect, position_topleft:pygame.Vector2):
        new_rectangle = area.copy()
        new_rectangle.topleft = position_topleft
        return new_rectangle