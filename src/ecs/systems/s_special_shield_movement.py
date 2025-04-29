import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_special_shield import CTagSpecialShield

def system_special_shield_movement(world: esper.World, entity_player: int):
    components = world.get_components(CTransform, CTagSpecialShield)
    player_transform = world.component_for_entity(entity_player, CTransform)

    for _, (c_transform, _) in components:
        c_transform.position.x = player_transform.position.x - 6
        c_transform.position.y = player_transform.position.y - 10