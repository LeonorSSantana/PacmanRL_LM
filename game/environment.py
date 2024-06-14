from __future__ import annotations
from operator import add

import numpy as np
from gymnasium.spaces import Discrete
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall, Lava
from minigrid.minigrid_env import MiniGridEnv
import pygame

from .custom_sprite import CustomSprite
from .maze import maze_walls
import random

# Asset paths
PACMAN_IMAGE_PATH = 'assets/images/pacman.png'
GHOST_IMAGE_PATHS = {
    'red': 'assets/images/ghosts/red.png',
    'blue': 'assets/images/ghosts/blue.png',
    'purple': 'assets/images/ghosts/purple.png',
    'yellow': 'assets/images/ghosts/yellow.png'
}
PELLET_IMAGE_PATH = 'assets/images/orb.png'


class PacmanEnv(MiniGridEnv):
    def __init__(self, grid_size=24, agent_start_pos=(1, 1), agent_start_dir=0, n_pellets=15, n_ghosts=8,
                 max_steps=None, mode='Manual', **kwargs):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir
        self.cumulative_reward = 0
        self.mode = mode

        # Define the mission
        mission_space = MissionSpace(mission_func=lambda: f"Mode: {self.mode} "
                                                          f" Cumulative Reward: {self.cumulative_reward}")

        if max_steps is None:
            max_steps = 4 * grid_size ** 2

        super(PacmanEnv, self).__init__(
            mission_space=mission_space,
            grid_size=grid_size,
            max_steps=max_steps,
            see_through_walls=True,
            render_mode='human',
            highlight=False,
            **kwargs
        )

        # Environment-specific properties
        self.action_space = Discrete(4)  # Actions: turn left, turn right, move forward and pick up pellet
        self.n_ghosts = n_ghosts
        self.n_pellets = n_pellets

        # Load custom images
        self.pacman_image = pygame.image.load(PACMAN_IMAGE_PATH).convert_alpha()
        self.pellet_image = pygame.image.load(PELLET_IMAGE_PATH).convert_alpha()
        self.ghost_images = {color: pygame.image.load(path).convert_alpha() for color, path in
                             GHOST_IMAGE_PATHS.items()}
        self.agent_image = pygame.transform.rotate(self.pacman_image, -90 * self.agent_start_dir)

    def _gen_grid(self, width, height):
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Create a Pacman-like maze structure
        self.__create_maze()

        # Place goals (pellets) throughout the maze
        self.__place_goals(n_pellets=30)

        # Place the agent (Pacman)
        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir

        # Place dynamic obstacles (ghosts) with different colors
        self.obstacles = []
        ghost_colors = ['red', 'blue', 'purple', 'yellow']

        # Creating and placing ghosts with different colors
        for i in range(self.n_ghosts):
            color = ghost_colors[i % len(ghost_colors)]
            ghost_image = pygame.transform.rotate(self.ghost_images[color], 90)  # Rotate image 90 degrees to the right
            ghost = CustomSprite(Lava(), ghost_image, color)  # Using Lava for ghosts
            self.obstacles.append(ghost)
            self.place_obj(ghost)

    def __place_goals(self, n_pellets):
        """
        Randomly place goals (pellets) around the grid in open spaces.
        """
        for _ in range(n_pellets):
            self.place_obj(CustomSprite(Goal(), self.pellet_image), max_tries=100)

    def __create_maze(self):
        """
        Create a Pacman-like maze. This function sets walls in a pattern similar to the original Pacman maze.
        The maze should be symmetrical and have pathways with enough space for Pacman to navigate.
        """
        for x, y, length, direction in maze_walls:
            if direction == 'vertical':
                for i in range(length):
                    self.grid.set(x, y + i, Wall())
            elif direction == 'horizontal':
                for i in range(length):
                    self.grid.set(x + i, y, Wall())

    def step(self, action):
        # Invalid action check
        if action not in self.action_space:
            action = 0

        # Helper variables
        front_cell = self.grid.get(*self.front_pos)
        not_clear = front_cell and front_cell.type == "wall"

        # Update obstacle (ghost) positions without diagonal movement
        for obstacle in self.obstacles:
            old_pos = obstacle.cur_pos

            # Determine a random direction for the ghost to move (up, down, left, or right)
            directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]
            valid_move = False

            while not valid_move and directions:
                move = random.choice(directions)
                directions.remove(move)
                new_pos = tuple(map(add, old_pos, move))

                if self.__is_in_bounds(new_pos) and self.grid.get(*new_pos) is None:
                    self.grid.set(new_pos[0], new_pos[1], obstacle)
                    self.grid.set(old_pos[0], old_pos[1], None)
                    obstacle.cur_pos = new_pos
                    valid_move = True

        # Update agent's position/direction
        obs, reward, terminated, truncated, info = super(PacmanEnv, self).step(action)

        # Check if the agent has collided with a ghost
        if any(obstacle.cur_pos == self.agent_pos for obstacle in self.obstacles):
            reward = -10
            terminated = True

        # Check if the agent faces a ghost and terminate the game
        if front_cell and front_cell.type == 'lava':  # Assuming ghosts are represented by 'Lava'
            reward = -10
            terminated = True

        # Check if the agent tries to move into a wall
        if action == self.actions.forward and not_clear:
            reward = -1
            terminated = False

        # Check if the agent visits a goal cell and reward accordingly
        current_cell = self.grid.get(*self.agent_pos)
        if current_cell and current_cell.type == 'goal':
            # Remove the goal from the grid
            self.grid.set(self.agent_pos[0], self.agent_pos[1], None)
            reward = 3
            terminated = False  # Do not terminate the game for collecting a goal

        # Update cumulative reward
        self.cumulative_reward += reward

        # Update the mission text to reflect the new reward
        self.mission = f"Cumulative Rewards: {self.cumulative_reward}"

        return obs, reward, terminated, truncated, info

    def __is_in_bounds(self, pos):
        """
        Check if the given position is within the grid boundaries.
        """
        x, y = pos
        return 0 <= x < self.grid.width and 0 <= y < self.grid.height

    # Custom rendering function
    def render(self):
        img = self.get_frame(self.highlight, self.tile_size, self.agent_pov)

        if self.render_mode == "human":
            img = np.transpose(img, axes=(1, 0, 2))
            if self.render_size is None:
                self.render_size = img.shape[:2]
            if self.window is None:
                pygame.init()
                pygame.display.init()
                self.window = pygame.display.set_mode(
                    (self.screen_size, self.screen_size)
                )
                pygame.display.set_caption("PacmanRL: Reinforcement Learning for Pacman")
            if self.clock is None:
                self.clock = pygame.time.Clock()
            surf = pygame.surfarray.make_surface(img)

            # Draw the agent with the custom sprite
            agent_tile_size = self.tile_size
            agent_x, agent_y = self.agent_pos
            agent_dir = self.agent_dir

            # Rotate the agent image to align with the current direction
            rotated_agent_image = pygame.transform.rotate(self.agent_image, -90 * agent_dir)
            agent_image = pygame.transform.scale(rotated_agent_image, (agent_tile_size, agent_tile_size))

            # Calculate the pixel position of the agent on the surface
            agent_px_x = agent_x * self.tile_size
            agent_px_y = agent_y * self.tile_size

            # Blit the agent image onto the surface
            surf.blit(agent_image, (agent_px_x, agent_px_y))

            # Create background with mission description
            offset = surf.get_size()[0] * 0.1
            bg = pygame.Surface(
                (int(surf.get_size()[0] + offset), int(surf.get_size()[1] + offset))
            )
            bg.convert()
            bg.fill((0, 0, 0))
            bg.blit(surf, (offset / 2, 0))

            bg = pygame.transform.smoothscale(bg, (self.screen_size, self.screen_size))

            font_size = 22
            text = self.mission
            font = pygame.freetype.SysFont("Calibri", font_size)
            text_rect = font.get_rect(text, size=font_size)
            text_rect.center = bg.get_rect().center
            text_rect.y = bg.get_height() - font_size * 1.5
            font.render_to(bg, text_rect, text, fgcolor=(255, 255, 255), size=font_size)

            self.window.blit(bg, (0, 0))
            pygame.event.pump()
            self.metadata["render_fps"] = 30
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

        elif self.render_mode == "rgb_array":
            return img
