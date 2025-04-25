from typing import Callable
import pygame
import esper

from src.ecs.components.c_input_command import CInputCommand, CommandPhase

def system_input_player(world: esper.World, event: pygame.event.Event, do_action:Callable[[CInputCommand, pygame.event.Event], None]):
    components = world.get_component(CInputCommand)
    for _,c_input in components:
        if event.type == pygame.KEYDOWN and c_input.key == event.key:
            c_input.phase = CommandPhase.START
            do_action(c_input, None)
        elif event.type == pygame.KEYUP and c_input.key == event.key:
            c_input.phase = CommandPhase.END
            do_action(c_input, None)
        elif event.type == pygame.MOUSEBUTTONDOWN and c_input.key != pygame.K_p:
            c_input.phase = CommandPhase.START
            do_action(c_input, event)
        elif event.type == pygame.MOUSEBUTTONUP and c_input.key != pygame.K_p:
            c_input.phase = CommandPhase.END
            do_action(c_input, event)