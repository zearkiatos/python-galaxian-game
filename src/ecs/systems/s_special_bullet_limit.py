import esper
import pygame

from src.ecs.components.c_special_bullet import CSpecialBullet
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_special_bullet import CTagSpecialBullet

def system_special_bullet_limit(world: esper.World):
    components = world.get_components(CTransform, CSurface, CTagSpecialBullet)
    MAXIMUN_X_DISTANCE = 50

    c_transform:CTransform
    c_surface:CSurface
    for entity, (c_transform,c_surface,_) in components:
        bullet = world.component_for_entity(entity, CSpecialBullet)
        if c_transform.position.x < bullet.start_position.x - MAXIMUN_X_DISTANCE or c_transform.position.x > bullet.start_position.x + MAXIMUN_X_DISTANCE:
            world.delete_entity(entity)