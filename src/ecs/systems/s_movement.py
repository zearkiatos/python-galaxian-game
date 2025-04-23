import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity

def system_movement(world: esper.World, delta_time:float):
    components = world.get_components(CTransform, CVelocity)

    c_transform:CTransform
    c_velocity:CVelocity
    for _, (c_transform, c_velocity) in components:
        c_transform.position.x += c_velocity.velocity.x * delta_time
        c_transform.position.y += c_velocity.velocity.y * delta_time
        
