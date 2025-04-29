import esper
from src.ecs.components.c_state_special import CStateSpecial, StateSpecial
from src.ecs.components.c_surface import CSurface

def system_special_shield_limit(world: esper.World, special_shield_state: CStateSpecial, entity_shield: int, current_time: float):
    if special_shield_state.state == StateSpecial.IDLE:
        time_passed = current_time - special_shield_state.start_time
        if time_passed >= special_shield_state.duration_time:
            world.delete_entity(entity_shield)
            special_shield_state.state = StateSpecial.NONE