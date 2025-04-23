import esper
import pygame
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_enemy_hunter import CTagEnemyHunter


def system_hunter_limit(world: esper.World, screen: pygame.Surface) -> None:
    screen_reactangle = screen.get_rect()
    components = world.get_components(CTransform, CVelocity, CSurface, CTagEnemyHunter)

    c_transform: CTransform
    c_velocity: CVelocity
    c_surface: CSurface
    c_tag_enemy_hunter: CTagEnemyHunter
    for _, (c_transform, c_velocity, c_surface, _) in components:
        hunter_sprite = CSurface.get_area_relative(c_surface.area, c_transform.position)
        if not screen_reactangle.contains(hunter_sprite):
            hunter_sprite.clamp_ip(screen_reactangle)
            c_transform.position.xy = hunter_sprite.topleft