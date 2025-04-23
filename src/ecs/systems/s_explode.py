import esper

from src.ecs.components.c_animation import CAnimation
from src.ecs.components.tags.c_tag_explosion import CTagExplosion


def system_explode(world: esper.World):
    components = world.get_components(CAnimation, CTagExplosion)

    for entity, (c_animation, _) in components:
        for animation in c_animation.animations_list:
            if c_animation.current_frame == animation.end:
                world.delete_entity(entity)
                break