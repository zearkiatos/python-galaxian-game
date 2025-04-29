import pygame
import esper
from src.ecs.components.c_state_special import CStateSpecial, StateSpecial
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_text import CTagText
from src.engine.service_locator import ServiceLocator


def system_special_counter(world: esper.World, interface_config: dict, entity_special: int, current_time: float, state: CStateSpecial):
    font = ServiceLocator.fonts_service.get(
        interface_config["font"], interface_config["size"])
    r, g, b = tuple(interface_config["color"].values())
    position = pygame.Vector2(tuple(interface_config["position"].values()))
    surface = world.component_for_entity(entity_special, CSurface)
    if state.state == StateSpecial.IDLE or state.state == StateSpecial.NONE:
        time_passed = current_time - state.start_time
        percentage = int((time_passed / state.restrict_seconds)* 100)
        if  time_passed > state.restrict_seconds:
            state.state = StateSpecial.ACTIVE
            state.start_time = 0.0
            text_surface = font.render(
                f"100%", True, pygame.Color(r, g, b))
            surface.surface = text_surface
        else:
            text_surface = font.render(
                f"{percentage}%", True, pygame.Color(255, 0, 0))
            surface.surface = text_surface

    entity = world.create_entity()
    world.add_component(entity, CTagText(interface_config["text"]))
    world.add_component(entity, CTransform(position))
