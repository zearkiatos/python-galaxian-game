import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_surface import CSurface

def system_animation(world: esper.World, delta_time: float):
    components = world.get_components(CSurface, CAnimation)

    for _, (c_surface, c_animation) in components:
        # 1. Decrease the value of the current_time of the animation
        c_animation.current_animation_time -= delta_time
        # 2. When current_time <=0,  we change the frame
        if c_animation.current_animation_time <= 0:
            # Restart the time
            c_animation.current_animation_time = c_animation.animations_list[c_animation.current_animation].framerate
            # Change the frame
            c_animation.current_frame += 1
            # 3. Limite the frame with its own start and end
            if c_animation.current_frame > c_animation.animations_list[c_animation.current_animation].end:
                c_animation.current_frame = c_animation.animations_list[c_animation.current_animation].start
            
        # 4. Calculate the new rectangle's sub area sprite
        rectangle_surface = c_surface.surface.get_rect()
        c_surface.area.w = rectangle_surface.w / c_animation.number_frames
        c_surface.area.x = c_surface.area.w * c_animation.current_frame