import pygame
import esper
import asyncio
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.create.prefabric_creator import create_bullet_square, create_enemy_spawner, create_input_player, create_player_square
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_bullet_limit import system_bullet_limit
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_explode import system_explode
from src.ecs.systems.s_hunter_chase import system_hunter_chase
from src.ecs.systems.s_hunter_limit import system_hunter_limit
from src.ecs.systems.s_hunter_state import system_hunter_state
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limit import system_player_limit
from src.ecs.systems.s_player_state import system_player_state
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_screen_bounce import system_screen_bounce
from src.ecs.systems.s_enemy_spawner import system_enemy_spawner
from src.utils.file_handler import read_json_file
from src.ecs.components.c_velocity import CVelocity
from src.config.config import Config


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()
        pygame.init()
        pygame.display.set_caption(self.window_config["title"])
        sizes = tuple(self.window_config["size"].values())
        self.config = Config()
        background_color = tuple(self.window_config["bg_color"].values())
        if not self.config.PYGBAG:
            self.screen = pygame.display.set_mode(sizes, pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode(sizes, 0)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config["framerate"]
        self.delta_time = 0
        self.bg_color = pygame.Color(background_color)

        self.ecs_world = esper.World()

    async def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
            await asyncio.sleep(0)
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, self.player_config, self.levels_config["player_spawn"])
        self._player_component_velocity = self.ecs_world.component_for_entity(self._player_entity, CVelocity)
        self._player_component_transform = self.ecs_world.component_for_entity(self._player_entity, CTransform)
        self._player_component_surface = self.ecs_world.component_for_entity(self._player_entity, CSurface)
        create_enemy_spawner(self.ecs_world, self.levels_config)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        self.clock.tick(self.framerate)
        self.delta_time = self.clock.get_time() / 1000.0

    def _process_events(self):
        for event in pygame.event.get():
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:
                self.is_running = False

    def _update(self):
        system_movement(self.ecs_world, self.delta_time)
        system_player_state(self.ecs_world)
        system_hunter_state(self.ecs_world)
        system_screen_bounce(self.ecs_world, self.screen)
        system_enemy_spawner(self.ecs_world, self.enemies_config, self.delta_time)
        system_collision_player_enemy(self.ecs_world, self._player_entity, self.levels_config, self.explosion_config)
        system_collision_bullet_enemy(self.ecs_world, self.explosion_config)
        self.block_bullet = system_bullet_limit(self.ecs_world, self.levels_config["player_spawn"], self.screen)
        system_player_limit(self.ecs_world, self.screen)
        system_hunter_limit(self.ecs_world, self.screen)
        system_animation(self.ecs_world, self.delta_time)
        system_hunter_chase(self.ecs_world, self.enemies_config, self._player_entity)
        system_explode(self.ecs_world)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        self.screen.fill(self.bg_color)
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()
    
    def _load_config_files(self):
        self.window_config = read_json_file("assets/cfg/window.json")
        self.enemies_config = read_json_file("assets/cfg/enemies.json")
        self.levels_config = read_json_file("assets/cfg/level_01.json")
        self.player_config = read_json_file("assets/cfg/player.json")
        self.bullet_config = read_json_file("assets/cfg/bullet.json")
        self.explosion_config = read_json_file("assets/cfg/explosion.json")

    def _do_action(self, c_input: CInputCommand, event: pygame.event.Event):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.x -= self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.x += self.player_config["input_velocity"]
        
        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.x += self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.x -= self.player_config["input_velocity"]
        
        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.y -= self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.y += self.player_config["input_velocity"]

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.y += self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.y -= self.player_config["input_velocity"]
        
        if c_input.name == "PLAYER_FIRE":
            if (c_input.phase == CommandPhase.START):
                if not self.block_bullet:
                    create_bullet_square(self.ecs_world, self.bullet_config, self._player_entity, event.pos)
