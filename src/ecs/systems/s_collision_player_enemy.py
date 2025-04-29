import esper

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.create.prefabric_creator import create_explosion

def system_collision_player_enemy(world:esper.World, player_entity:int, levels_config:dict, explosion_config:dict) -> None:
    components = world.get_components(CSurface, CTransform, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    player_rectangle = CSurface.get_area_relative(player_surface.area, player_transform.position)
    initial_x, initial_y = tuple(levels_config["player_spawn"]["position"].values())

    for enemy_entity, (c_surface, c_transform, _) in components:
        enemy_rectangle = CSurface.get_area_relative(c_surface.area, c_transform.position)
        if enemy_rectangle.colliderect(player_rectangle):
            world.delete_entity(enemy_entity)
            create_explosion(world, c_transform.position.copy(), explosion_config)
            player_transform.position.x = initial_x - player_surface.area.width / 2
            player_transform.position.y = initial_y - player_surface.area.height / 2
