import esper
import pygame

from src.ecs.components.c_enemy_spawner import CEnemySpawner, SpawnEventData
from src.ecs.components.c_hunter import CHunter
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy_hunter import CTagEnemyHunter
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def system_hunter_chase(world: esper.World, enemy_info: dict, player_entity: int):
    hunter_components = world.get_components(
        CVelocity, CSurface, CTransform, CHunter)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    player_rectangle = CSurface.get_area_relative(
        player_surface.area, player_transform.position)

    for _, (hunter_velocity, _, hunter_transform, c_hunter) in hunter_components:
        distance_to_player = (player_transform.position - hunter_transform.position).length()
        distance_to_initial = (c_hunter.initial_position - hunter_transform.position).length()

        if distance_to_player <= enemy_info["Hunter"]["distance_start_chase"]:
            direction = (player_transform.position - hunter_transform.position).normalize()
            hunter_velocity.velocity = direction * enemy_info["Hunter"]["velocity_chase"]
            ServiceLocator.sounds_service.play(enemy_info["Hunter"]["sound_chase"])
        elif distance_to_player >= enemy_info["Hunter"]["distance_start_return"]:
            if distance_to_initial > 1:
                direction = (c_hunter.initial_position - hunter_transform.position).normalize()
                hunter_velocity.velocity = direction * enemy_info["Hunter"]["velocity_return"]
            else:
                hunter_velocity.velocity = pygame.Vector2(0, 0)