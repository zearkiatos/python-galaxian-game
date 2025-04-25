import random
import esper
import pygame

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_explosion_state import CExplosionState
from src.ecs.components.c_hunter import CHunter
from src.ecs.components.c_hunter_state import CHunterState
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_player_state import CPlayerState
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_enemy_asteroid import CTagEnemyAsteroid
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator


def create_square(world: esper.World, size: pygame.Vector2, position: pygame.Vector2, velocity: pygame.Vector2, color: pygame.Color) -> int:
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(
        size, color))
    world.add_component(
        square_entity, CTransform(position))
    world.add_component(
        square_entity, CVelocity(velocity))

    return square_entity


def create_sprite(world: esper.World, position: pygame.Vector2, velocity: pygame.Vector2, surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CTransform(position))
    world.add_component(sprite_entity, CVelocity(velocity))
    world.add_component(sprite_entity, CSurface.from_surface(surface))

    return sprite_entity


def create_hunter_enemy(world: esper.World, position: pygame.Vector2, enemy_info: dict):
    enemy_sprite = ServiceLocator.images_service.get(enemy_info["image"])
    velocity = pygame.Vector2(0, 0)
    enemy_entity = create_sprite(world, position, velocity, enemy_sprite)
    world.add_component(enemy_entity, CTagEnemy("Hunter"))
    world.add_component(enemy_entity, CAnimation(enemy_info["animations"]))
    world.add_component(enemy_entity, CHunterState(position))

def create_explosion(world: esper.World, position: pygame.Vector2, explosion_config: dict):
    explosion_sprite = ServiceLocator.images_service.get(explosion_config["image"])
    velocity = pygame.Vector2(0, 0)
    explosion_entity = create_sprite(world, position, velocity, explosion_sprite)
    world.add_component(explosion_entity, CTagExplosion())
    world.add_component(explosion_entity, CAnimation(explosion_config["animations"]))
    ServiceLocator.sounds_service.play(explosion_config["sound"])
    return explosion_entity


def create_enemy_square(world: esper.World, position: pygame.Vector2, enemy_info: dict):
    enemy_surface = ServiceLocator.images_service.get(enemy_info["image"])
    velocity_max = enemy_info.get("velocity_max", 0) or 0
    velocity_min = enemy_info.get("velocity_min", 0) or 0
    velocity = pygame.Vector2(0, 0)
    if velocity_max > 0 and velocity_min > 0:
        velocity_range = random.randrange(velocity_min, velocity_max)
        velocity = pygame.Vector2(
            random.choice([-velocity_range, velocity_range]),
            random.choice([-velocity_range, velocity_range])
        )

    enemy_entity = create_sprite(world, position, velocity, enemy_surface)
    world.add_component(enemy_entity, CTagEnemy("Bouncer"))
    world.add_component(enemy_entity, CTagEnemyAsteroid())
    ServiceLocator.sounds_service.play(enemy_info["sound"])
    return enemy_entity


def create_enemy_spawner(world: esper.World, level_data: dict):
    spawner_entity = world.create_entity()
    world.add_component(spawner_entity, CEnemySpawner(
        level_data['enemy_spawn_events']))


def create_player_square(world: esper.World, player_info: dict, player_level_info: dict) -> int:
    player_sprite = ServiceLocator.images_service.get(player_info["image"])
    size = player_sprite.get_size()
    size = (size[0] / player_info["animations"]["number_frames"], size[1])
    x, y = tuple(player_level_info["position"].values())
    position = pygame.Vector2(x - (size[0]/2), y - (size[1]/2))
    velocity = pygame.Vector2(0, 0)

    player_entity = create_sprite(world, position, velocity, player_sprite)
    world.add_component(player_entity, CTagPlayer())
    world.add_component(player_entity, CAnimation(player_info["animations"]))
    world.add_component(player_entity, CPlayerState())
    return player_entity


def create_input_player(world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_WASD_left = world.create_entity()
    input_WASD_right = world.create_entity()
    input_WASD_up = world.create_entity()
    input_WASD_down = world.create_entity()
    input_right_mouse = world.create_entity()
    input_pause = world.create_entity()
    world.add_component(input_left, CInputCommand(
        "PLAYER_LEFT", pygame.K_LEFT))
    world.add_component(input_right, CInputCommand(
        "PLAYER_RIGHT", pygame.K_RIGHT))
    world.add_component(input_up, CInputCommand("PLAYER_UP", pygame.K_UP))
    world.add_component(input_down, CInputCommand(
        "PLAYER_DOWN", pygame.K_DOWN))
    world.add_component(input_WASD_left, CInputCommand(
        "PLAYER_LEFT", pygame.K_a))
    world.add_component(input_WASD_right, CInputCommand(
        "PLAYER_RIGHT", pygame.K_d))
    world.add_component(input_WASD_up, CInputCommand("PLAYER_UP", pygame.K_w))
    world.add_component(input_WASD_down, CInputCommand(
        "PLAYER_DOWN", pygame.K_s))
    world.add_component(input_right_mouse, CInputCommand(
        "PLAYER_FIRE", pygame.BUTTON_RIGHT))
    world.add_component(input_pause, CInputCommand("PAUSE", pygame.K_p))


def create_bullet_square(world: esper.World, bullet_info: dict, player_entity: int, mouse_position: pygame.Vector2) -> int:
    bullet_surface = ServiceLocator.images_service.get(bullet_info["image"])
    player_position = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)
    bullet_size = bullet_surface.get_rect().size
    position = pygame.Vector2(
        player_position.position.x +
        player_surface.area.size[0]/2 - (bullet_size[0]/2),
        player_position.position.y +
        player_surface.area.size[1]/2 - (bullet_size[1]/2)
    )
    direction = (mouse_position - position).normalize()

    velocity = pygame.Vector2(direction.x * bullet_info["velocity"],
                              direction.y * bullet_info["velocity"])

    bullet_entity = create_sprite(
        world, position, velocity, bullet_surface)
    world.add_component(bullet_entity, CTagBullet())
    ServiceLocator.sounds_service.play(bullet_info["sound"])
    return bullet_entity

def create_text(world: esper.World, interface_config: dict, position: pygame.Vector2 = None) -> int:
    font = ServiceLocator.fonts_service.get(interface_config["font"], interface_config["size"])
    r,g,b = tuple(interface_config["color"].values())
    if not position:
        if interface_config["position"] is None:
            position = pygame.Vector2(0, 0)
        else:
            position = pygame.Vector2(tuple(interface_config["position"].values()))
    else:
        position = pygame.Vector2(position.x, position.y)
    text_surface = font.render(
        interface_config["text"], True, pygame.Color(r,g,b))
    entity = world.create_entity()
    world.add_component(entity, CTransform(position))
    world.add_component(entity, CSurface.from_surface(text_surface))

    return entity
    

    