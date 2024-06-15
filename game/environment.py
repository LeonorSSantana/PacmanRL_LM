import sys
from collections import deque
from operator import add

import numpy as np
from gymnasium.spaces import Discrete
from minigrid.core.constants import DIR_TO_VEC
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
    """
    Custom environment class for the Pacman game. This class extends the MiniGrid environment and provides a custom
    implementation of the Pacman game with ghosts and pellets. The environment is designed to be used with the
    Q-Learning and SARSA agents for training and evaluation.
    """

    def __init__(self, grid_size=24, agent_start_pos=(1, 1), agent_start_dir=0, n_pellets=30, n_ghosts=4,
                 max_steps=1000, mode='Manual', algorithm=None, frames_per_second=10, seed=None, **kwargs):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir
        self.cumulative_reward = 0
        self.mode = mode
        self.algorithm = algorithm
        self.seed = seed
        self.frames_per_second = frames_per_second

        # Define the mission string
        self.mission_string = f"Mode: {self.mode}, Cumulative Reward: {self.cumulative_reward}" \
            if self.mode == "Manual" else f"Algorithm: {self.algorithm}, Cumulative Reward: {self.cumulative_reward}"

        # Define the mission
        mission_space = MissionSpace(mission_func=lambda: self.mission_string)

        if max_steps is None:
            max_steps = 4 * grid_size ** 2

        super().__init__(
            mission_space=mission_space,
            grid_size=grid_size,
            max_steps=max_steps,
            see_through_walls=True,
            render_mode='human',
            highlight=False,
            **kwargs
        )

        # Environment-specific properties
        # self.action_space = Discrete(4)  # Actions: turn left, turn right, move forward and pick up pellet
        self.action_space = Discrete(3)  # Actions: turn left, turn right, move forward
        self.n_ghosts = n_ghosts
        self.n_pellets = n_pellets

        # Load custom images
        self.pacman_image = pygame.image.load(PACMAN_IMAGE_PATH).convert_alpha()
        self.pellet_image = pygame.image.load(PELLET_IMAGE_PATH).convert_alpha()
        self.ghost_images = {color: pygame.image.load(path).convert_alpha() for color, path in GHOST_IMAGE_PATHS.items()}
        self.agent_image = pygame.transform.rotate(self.pacman_image, -90 * self.agent_start_dir)

    def _gen_grid(self, width, height):
        """
        Generate the grid for the environment.
        :param width: The width of the grid
        :param height: The height of the grid
        """
        self.grid = Grid(width, height)

        # Generate the surrounding walls
        self.grid.wall_rect(0, 0, width, height)

        # Create a Pacman-like maze structure
        self.__create_maze()

        # Place goals (pellets) throughout the maze
        self.__place_pellets(n_pellets=self.n_pellets)

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

            # Ensure that the ghost's current position is set after placing it
            ghost.obj.cur_pos = ghost.obj.init_pos if ghost.obj.init_pos else self._rand_pos(1, width - 1, 1, height - 1)

    def __place_pellets(self, n_pellets):
        """
        Randomly place goals (pellets) around the grid in open spaces.
        :param n_pellets: The number of pellets to place in the grid
        """
        for _ in range(n_pellets):
            self.place_obj(CustomSprite(Goal(), self.pellet_image), max_tries=100)

    def __create_maze(self):
        """
        Create a Pacman-like maze. This function sets walls in a pattern similar to the original Pacman maze.
        """
        for x, y, length, direction in maze_walls:
            if direction == 'vertical':
                for i in range(length):
                    self.grid.set(x, y + i, Wall())
            elif direction == 'horizontal':
                for i in range(length):
                    self.grid.set(x + i, y, Wall())

    def __is_in_bounds(self, pos):
        """
        Check if the given position is within the grid boundaries.
        """
        x, y = pos
        return 0 <= x < self.grid.width and 0 <= y < self.grid.height

    def get_state(self):
        """
        Get the current state representation for the agent.
        The state includes:
        - Agent's position and direction
        - Relative positions of the nearest pellet and ghost
        - Distance to the nearest wall
        """
        state = {
            'agent_pos': self.agent_pos,
            'agent_dir': self.agent_dir,
            'nearest_pellet': self._nearest_pellet(),
            'nearest_ghost': self._nearest_ghost(),
        }
        # Convert dictionary to a sorted tuple of items to make it hashable
        return tuple(sorted(state.items()))

    @staticmethod
    def bfs_nearest_object(agent_pos, grid, target_type):
        """
        Perform BFS to find the nearest object of the specified type.
        :param agent_pos: Current position of the agent.
        :param grid: The grid containing the objects.
        :param target_type: The type of target object to find.
        :return: The relative position of the nearest object or (0, 0) if none is found.
        """
        width, height = grid.width, grid.height
        queue = deque([(agent_pos, 0)])  # Each entry is (position, distance)
        visited = set()
        visited.add(agent_pos)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Possible movements: down, right, up, left

        while queue:
            (x, y), dist = queue.popleft()

            # Check all adjacent cells
            for dx, dy in directions:
                nx, ny = x + dx, y + dy

                if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in visited:
                    cell = grid.get(nx, ny)
                    if cell is not None:
                        if cell.type == target_type:
                            return nx - agent_pos[0], ny - agent_pos[1]  # Return relative position
                        if cell.type == 'wall':
                            continue  # Skip walls

                    visited.add((nx, ny))
                    queue.append(((nx, ny), dist + 1))

        return 0, 0  # Return (0, 0) if no target object is found

    def _nearest_pellet(self):
        """
        Calculate the relative position of the nearest pellet.
        """
        return self.bfs_nearest_object(self.agent_pos, self.grid, 'goal')

    def _nearest_ghost(self):
        """
        Calculate the relative position of the nearest ghost.
        """
        return self.bfs_nearest_object(self.agent_pos, self.grid, 'lava')

    def __calculate_rewards(self, action):
        reward = 0
        terminated = False

        # Helper variables
        front_cell = self.grid.get(*self.front_pos)

        # Check if the agent attempts to move into a wall
        if action == self.actions.forward and front_cell is not None and front_cell.type == 'wall':
            reward -= 1

        # Reward for reaching the pellet
        current_cell = self.grid.get(*self.agent_pos)
        if current_cell and current_cell.type == 'goal':
            reward += 50
            self.grid.set(self.agent_pos[0], self.agent_pos[1], None)

        # Penalty for hitting a ghost
        if any(obstacle.cur_pos == self.agent_pos for obstacle in self.obstacles):
            reward -= 100
            terminated = True

        # Penalty if front cell is a ghost
        if front_cell is not None and front_cell.type == 'lava':
            reward -= 100
            terminated = True

        # Penalize if the agent is spinning (moving left or right without progressing)
        nearest_pellet_pos = self._nearest_pellet()
        if nearest_pellet_pos != (0, 0):  # There is a pellet in the grid
            agent_pos = np.array(self.agent_pos)
            nearest_pellet_abs_pos = agent_pos + np.array(nearest_pellet_pos)

        # If the action is not forward, check if it brings agent closer to the nearest pellet
        if action in [self.actions.left, self.actions.right]:
            # Current distance to the nearest pellet
            agent_pos = np.array(self.agent_pos)
            nearest_pellet_abs_pos = agent_pos + np.array(nearest_pellet_pos)
            current_distance = np.linalg.norm(agent_pos - nearest_pellet_abs_pos)

            # Simulate the agent's new position after the action
            new_agent_dir = (self.agent_dir + (1 if action == self.actions.right else -1)) % 4
            direction_vec = DIR_TO_VEC[new_agent_dir]
            new_front_pos = self.agent_pos + direction_vec
            new_distance = np.linalg.norm(np.array(new_front_pos) - nearest_pellet_abs_pos)

            # Penalize if the new distance is not shorter
            if new_distance >= current_distance:
                reward -= 1

        return reward, terminated

    def step(self, action):
        """
        Execute the given action in the environment.
        :param action: The action to execute (0: turn left, 1: turn right, 2: move forward, 3: pick up pellet)
        :return: Tuple (obs, reward, terminated, truncated, info)
        """
        # Invalid action check
        if action not in self.action_space:
            action = 0

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
        obs, reward, terminated, truncated, info = super().step(action)

        # Call the reward function to calculate reward and termination
        reward, terminated = self.__calculate_rewards(action)

        # Update cumulative reward
        self.cumulative_reward += reward

        # Update the mission text to reflect the new reward
        self.mission = f"Mode: {self.mode}, Cumulative Reward: {self.cumulative_reward}" \
            if self.mode == "Manual" else f"Algorithm: {self.algorithm}, Cumulative Reward: {self.cumulative_reward}"

        return obs, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        # Call the parent reset method which initializes everything
        obs, info = super().reset(seed=self.seed, options=options)

        # Ensure the agent position and direction are initialized
        self.agent_pos = self.agent_start_pos
        self.agent_dir = self.agent_start_dir

        # Debugging print statements to verify reset
        print(f"[ENV] Agent reset to position: {self.agent_pos} with direction: {self.agent_dir}")
        self.cumulative_reward = 0

        return obs, info

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
            self.metadata["render_fps"] = self.frames_per_second
            self.clock.tick(self.metadata["render_fps"])
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        elif self.render_mode == "rgb_array":
            return img
