import esper

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

def system_hunter_state(world: esper.World, player_entity: int, hunter_info: dict):
    player_transform = world.component_for_entity(player_entity, CTransform)
    components = world.get_components(CHunterState, CAnimation, CTransform, CVelocity)

    for _, (c_hunter_state, c_animation, c_transform, c_velocity) in components:
        if c_hunter_state.state == HunterState.IDLE:
            _do_idle_state(c_hunter_state, c_animation, c_velocity, c_transform, player_transform, hunter_info)
        elif c_hunter_state.state == HunterState.MOVE:
            _do_move_state(c_hunter_state, c_animation, c_velocity, c_transform, player_transform, hunter_info)
            ServiceLocator.sounds_service.play(hunter_info["sound_chase"])
        elif c_hunter_state.state == HunterState.RETURN:
            _do_return_state(c_hunter_state, c_animation, c_velocity, c_transform, hunter_info)

def _do_idle_state(c_state: CHunterState, c_animation: CAnimation, c_velocity: CVelocity, c_transform: CTransform, player_transform: CTransform, hunter_info: dict):
    set_animation(c_animation, 1)
    c_velocity.velocity.x = 0
    c_velocity.velocity.y = 0

    distance_to_player = c_transform.position.distance_to(player_transform.position)

    if distance_to_player < hunter_info["distance_start_chase"]:
        c_state.state = HunterState.MOVE

def _do_move_state(c_state: CHunterState, c_animation: CAnimation, c_velocity: CVelocity, c_transform: CTransform, player_transform: CTransform,  hunter_info: dict):
    set_animation(c_animation, 0)

    c_velocity.velocity = (player_transform.position - c_transform.position).normalize() * hunter_info["velocity_chase"]

    distance_to_origin = c_state.start_position.distance_to(c_transform.position)

    if distance_to_origin >= hunter_info["distance_start_return"]:
        c_state.state = HunterState.RETURN

def _do_return_state(c_state: CHunterState, c_animation: CAnimation, c_velocity: CVelocity, c_transform: CTransform, hunter_info: dict):
    MINIMAL_DISTANCE = 2
    set_animation(c_animation, 0)
    c_velocity.velocity = (c_state.start_position - c_transform.position).normalize() * hunter_info["velocity_return"]
    distance_to_origin = c_state.start_position.distance_to(c_transform.position)

    if distance_to_origin <= MINIMAL_DISTANCE:
        c_transform.position.xy = c_state.start_position.xy
        c_state.state = HunterState.IDLE