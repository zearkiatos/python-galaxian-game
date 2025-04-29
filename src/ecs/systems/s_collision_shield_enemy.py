import esper

from src.ecs.components.c_state_special import StateSpecial
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.create.prefabric_creator import create_explosion

def system_collision_shield_enemy(world:esper.World, shield_entity:int, shield_state: StateSpecial, special_shield_info:dict, explosion_config:dict) -> None:
    if shield_state.state == StateSpecial.IDLE:
        distance_for_collision = special_shield_info["minimal_distance"]
        components = world.get_components(CSurface, CTransform, CTagEnemy)
        shield_transform = world.component_for_entity(shield_entity, CTransform)
        shield_surface = world.component_for_entity(shield_entity, CSurface)
        shield_rectangle = CSurface.get_area_relative(shield_surface.area, shield_transform.position)
        shield_rectangle_inflate = shield_rectangle.inflate(distance_for_collision * 2, distance_for_collision * 2)
        for enemy_entity, (c_surface, c_transform, _) in components:
            enemy_rectangle = CSurface.get_area_relative(c_surface.area, c_transform.position)
            if shield_rectangle_inflate.colliderect(enemy_rectangle):
                world.delete_entity(enemy_entity)
                create_explosion(world, c_transform.position.copy(), explosion_config)
                break
