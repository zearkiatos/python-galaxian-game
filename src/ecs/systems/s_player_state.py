import esper

from src.ecs.components.c_animation import CAnimation, set_animation
from src.ecs.components.c_player_state import CPlayerState, PlayerState
from src.ecs.components.c_velocity import CVelocity


def system_player_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CPlayerState)

    for _, (c_velocity, c_animation, c_player_state) in components:
        if c_player_state.state == PlayerState.IDLE:
            _do_idle_state(c_velocity, c_animation, c_player_state)
        elif c_player_state.state == PlayerState.MOVE:
            _do_move_state(c_velocity, c_animation, c_player_state)


def _do_idle_state(c_velocity: CVelocity, c_animation: CAnimation, c_player_state: CPlayerState):
    set_animation(c_animation, 1)

    if c_velocity.velocity.magnitude_squared() > 0:
        c_player_state.state = PlayerState.MOVE


def _do_move_state(c_velocity: CVelocity, c_animation: CAnimation, c_player_state: CPlayerState):
    set_animation(c_animation, 0)

    if c_velocity.velocity.magnitude_squared() <= 0:
        c_player_state.state = PlayerState.IDLE
