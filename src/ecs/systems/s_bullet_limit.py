import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_bullet_limit(world: esper.World, levels_config: dict, screen:pygame.Surface):
    screen_rectangle = screen.get_rect()
    components = world.get_components(CTransform, CSurface, CTagBullet)
    bullets_quantity = len(components)

    c_transform:CTransform
    c_surface:CSurface
    c_tag_bullet:CTagBullet
    for entity, (c_transform,c_surface,_) in components:
        bullet = CSurface.get_area_relative(c_surface.area, c_transform.position)
        if bullet.left < 0 or bullet.right > screen_rectangle.width:
            world.delete_entity(entity)
            bullets_quantity -= 1
            continue
        if bullet.top < 0 or bullet.bottom > screen_rectangle.height:
            world.delete_entity(entity)
            bullets_quantity -= 1
            continue
    return bullets_quantity >= levels_config["max_bullets"]