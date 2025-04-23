import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_hunter_state import CHunterState, HunterState
from src.ecs.components.c_velocity import CVelocity

def system_hunter_state(world: esper.World):
    components = world.get_components(CVelocity, CAnimation, CHunterState)

    for _, (c_velocity, c_animation, c_hunter_state) in components:
        if c_hunter_state.state == HunterState.IDLE:
            _do_idle_state(c_velocity, c_animation, c_hunter_state)
        elif c_hunter_state.state == HunterState.MOVE:
            _do_move_state(c_velocity, c_animation, c_hunter_state)

def _do_idle_state(c_velocity: CVelocity, c_animation: CAnimation, c_hunter_state: CHunterState):
    _set_animation(c_animation, 1)

    if c_velocity.velocity.magnitude_squared() > 0:
        c_hunter_state.state = HunterState.MOVE

def _do_move_state(c_velocity: CVelocity, c_animation: CAnimation, c_hunter_state: CHunterState):
    _set_animation(c_animation, 0)

    if c_velocity.velocity.magnitude_squared() <= 0:
        c_hunter_state.state = HunterState.IDLE

def _set_animation(c_animation: CAnimation, animation_number: int):
    if c_animation.current_animation == animation_number:
        return

    c_animation.current_animation = animation_number
    c_animation.current_animation_time = 0

    c_animation.current_frame = c_animation.current_frame = c_animation.animations_list[
        c_animation.current_animation].start