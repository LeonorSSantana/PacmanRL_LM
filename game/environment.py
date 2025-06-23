import sys
from collections import deque
from operator import add
from operator import itemgetter

import numpy as np
from gymnasium.spaces import Discrete
from minigrid.core.constants import DIR_TO_VEC
from minigrid.core.grid import Grid
from minigrid.core.mission import MissionSpace
from minigrid.core.world_object import Goal, Wall, Lava
from minigrid.minigrid_env import MiniGridEnv

import pygame
from pygame import freetype

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
                 max_steps=2000, mode='Manual', algorithm=None, frames_per_second=10, seed=None, **kwargs):
        self.agent_start_pos = agent_start_pos
        self.agent_start_dir = agent_start_dir
        self.cumulative_reward = 0
        self.mode = mode
        self.algorithm = algorithm
        self.seed = seed
        self.frames_per_second = frames_per_second
        self.visited_positions = set()
        self.position_history = deque(maxlen=10)
        self.pellets_in_a_row = 0
        self.predicted_ghost_path = []
        self.current_episode = 0


        # Environment-specific properties
        self.n_ghosts = n_ghosts
        self.n_pellets = n_pellets
        self.remaining_pellets = n_pellets

        # Define the mission string
        self.mission_string = f"Mode: {self.mode}        Reward: {self.cumulative_reward}        Pellets: {self.remaining_pellets}" \
            if self.mode == "Manual" else \
            f"Algorithm: {self.algorithm}       Reward: {self.cumulative_reward}        Pellets: {self.remaining_pellets}"

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
        self.action_space = Discrete(3)  # Actions: turn left, turn right, move forward

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
            ghost.obj.cur_pos = ghost.obj.init_pos if ghost.obj.init_pos else self._rand_pos(1, width - 1, 1,
                                                                                             height - 1)

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
        agent_pos = self.agent_pos
        agent_dir = self.agent_dir

        state = {
            'agent_pos': agent_pos,
            'agent_dir': agent_dir
            }
        
        # Convert dictionary to a sorted tuple of items to make it hashable
        return tuple(sorted(state.items()))
    
        #TENTATIVA DE MELHORAR O STATE MAS OS RESULTADOS PIORARAM
        #def get_state(self):
        """
        Get the current state representation for the agent.
        The state includes:
        - Agent's position and direction
        - Relative positions of the nearest pellet and ghost
        - Distance to the nearest wall
        """
        #agent_pos = self.agent_pos
        #agent_dir = self.agent_dir

        #pellet_rel = self._nearest_pellet()  # já retorna (dx, dy) relativo
        #ghost_rel = self._nearest_ghost()    # já retorna (dx, dy) relativo
                    #'pellet_rel': pellet_rel,
            #'ghost_rel': ghost_rel

        #state = {
            #'agent_pos': agent_pos,
            #'agent_dir': agent_dir,
            #'pellet_rel': pellet_rel,
            #'ghost_rel': ghost_rel}
        # Convert dictionary to a sorted tuple of items to make it hashable
        #return tuple(sorted(state.items()))

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
        queue = deque([(agent_pos, (0, 0))])  # Each entry is (position, distance)
        visited = set()
        visited.add(agent_pos)

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Possible movements: down, right, up, left

        while queue:
            (x, y), dist = queue.popleft()

            # Check all adjacent cells
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                if 0 <= nx < width and 0 <= ny < height and next_pos not in visited:
                    cell = grid.get(nx, ny)
                    # Skip walls only
                    if cell is not None and cell.type == 'wall':
                        continue

                    # Found the target
                    if cell is not None and cell.type == target_type:
                        return dist[0] + dx, dist[1] + dy  # Return relative to agent

                    visited.add(next_pos)
                    queue.append(((nx, ny), (dist[0] + dx,dist[1] + dy)))

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
    
    #NOVOS METODOS

    def _is_valid_position(self, pos):
        # Verifica se a posição está dentro dos limites do mapa e se não é uma parede.
        if not self.__is_in_bounds(pos):
            return False # Fora dos limites do mapa
        cell = self.grid.get(pos[0], pos[1])
        if cell is None:
            return False # Célula vazia (não existente)
        if cell.type == 'wall': 
            return False # Posição é uma parede, não pode passar
        return True # Posição é válida
    
    def _is_dead_end(self, pos):
        # Verifica se o agente está num beco sem saída.
        possible_moves = 0
        for direction_vec in DIR_TO_VEC:
            neighbor = (pos[0] + direction_vec[0], pos[1] + direction_vec[1])
            if self._is_valid_position(neighbor):
                possible_moves += 1
        return possible_moves <= 1 # Se houver só uma ou nenhuma saída, é um beco

    def _is_open_area(self, pos):
        # Verifica o agente está numa área aberta (>=3 caminhos disponíveis).
        possible_moves = 0
        for direction_vec in DIR_TO_VEC:
            neighbor = (pos[0] + direction_vec[0], pos[1] + direction_vec[1])
            if self._is_valid_position(neighbor):
                possible_moves += 1
        return possible_moves >= 3
    

    def __calculate_rewards(self, action):
        """
        Calculate the reward and termination conditions based on the current state and action.
        Reward points:
        - Penalty for each step (-1)
        - Reward for reaching the pellet (+50)
        - Penalty for hitting a ghost (-100)
        - Penalty if the new distance to the nearest pellet is greater than the current distance (-1)
        - Penalty if the agent is not facing the nearest pellet (-1)
        :param action: The action to execute (0: turn left, 1: turn right, 2: move forward)
        :return: Tuple (reward, terminated)
        """
        reward = -0.5 # Penalização por cada passo dado - ALTERADO DE 1 PARA 0.5
        terminated = False

        # Inicializar estruturas se necessário
        if not hasattr(self, 'visited_positions'):
            self.visited_positions = set()
        if not hasattr(self, 'position_history'):
            self.position_history = []
        if not hasattr(self, 'pellet_streak'):
            self.pellet_streak = 0
        if not hasattr(self, 'survival_steps'):
            self.survival_steps = 0

        # Helper variables
        front_cell = self.grid.get(*self.front_pos)

        # Check if the agent attempts to move into a wall
        if action == self.actions.forward and front_cell is not None and front_cell.type == 'wall':
            reward -= 0.7

        # Recompença por apanhar um pellet
        current_cell = self.grid.get(*self.agent_pos)
        if current_cell and current_cell.type == 'goal':
            if not hasattr(self, 'pellets_collected'):
                self.pellets_collected = 0

            base_reward = 100
            pellet_bonus = 5 * self.pellets_collected
            reward += base_reward + pellet_bonus

            self.pellets_collected += 1

            self.last_reward_was_pellet = True
            self.pellets_in_a_row = getattr(self, 'pellets_in_a_row', 0) + 1  # Se quiseres manter bónus por sequência
            self.grid.set(self.agent_pos[0], self.agent_pos[1], None)
            self.remaining_pellets -= 1


        is_ghost_collision = (
            any(obstacle.cur_pos == self.agent_pos for obstacle in self.obstacles) or
            (front_cell is not None and front_cell.type == 'lava')
        )

        if is_ghost_collision:
            if not hasattr(self, 'ghost_hits'):
                self.ghost_hits = 0

            self.ghost_hits += 1

            if self.ghost_hits < 3:
                reward -= 100
                terminated = False
            else:
                reward -= 100  # Penalidade também na 3ª colisão
                terminated = True

        # Calcular a posição do pellet mais próximo antes do agente agir
        nearest_pellet_pos = self._nearest_pellet()
        nearest_pellet_abs_pos = np.array(self.agent_pos) + np.array(nearest_pellet_pos)
        current_distance = np.linalg.norm(np.array(self.agent_pos) - nearest_pellet_abs_pos)

        # Calcular a nova posição e direção baseada na ação
        new_agent_pos = np.array(self.agent_pos)
        new_agent_dir = self.agent_dir

        if action == self.actions.left:
            new_agent_dir = (self.agent_dir - 1) % 4
        elif action == self.actions.right:
            new_agent_dir = (self.agent_dir + 1) % 4
        elif action == self.actions.forward:
            new_agent_pos = new_agent_pos + DIR_TO_VEC[self.agent_dir]

        new_agent_pos_tuple = tuple(new_agent_pos)

        # Calcular a nova front position e a distância para o pellet mais próximo depois da ação
        new_distance = np.linalg.norm(new_agent_pos - nearest_pellet_abs_pos)

        # Ajustar a nova distância se a ação for andar para a frente e o agente estiver exatamente em cima do pellet
        if action == self.actions.forward and np.array_equal(new_agent_pos, nearest_pellet_abs_pos):
            new_distance = 0  # No penalty if moving directly onto the pellet

        # Penalizar se a nova distância for maior do que a distância atual
        distance_penalized = False
        if new_distance > current_distance:
            reward -= 0.5
            distance_penalized = True
        elif new_distance < current_distance:
            reward += (current_distance - new_distance) * 0.5  # bónus proporcional

        # Penalizar se o agente não estiver virado para o pellet mais próximo
        # Determinar a direção do agente até ao pellet mais próximo
        direction_to_pellet = np.array(nearest_pellet_pos)
        direction_to_pellet = np.sign(direction_to_pellet)  # Get the direction vector in terms of unit steps

        # Map the direction vector to one of the cardinal directions (0: right, 1: down, 2: left, 3: up)
        if np.array_equal(direction_to_pellet, [1, 0]):
            desired_direction = 0  # Right
        elif np.array_equal(direction_to_pellet, [0, 1]):
            desired_direction = 1  # Down
        elif np.array_equal(direction_to_pellet, [-1, 0]):
            desired_direction = 2  # Left
        elif np.array_equal(direction_to_pellet, [0, -1]):
            desired_direction = 3  # Up
        else:
            desired_direction = self.agent_dir  # If pellet is on the agent or direction is indeterminate

        # Penalizar orientação incorreta apenas se não foi penalizado por se afastar
        if not distance_penalized and new_distance <= 3 and new_agent_dir != desired_direction:
            reward -= 0.2
        
        # Penalização por estar próximo de fantasmas
        ghost_rel = self._nearest_ghost()
        ghost_abs = np.array(self.agent_pos) + np.array(ghost_rel)
        ghost_distance = np.linalg.norm(np.array(self.agent_pos) - ghost_abs)

        if ghost_distance < 1.5:
            reward -= 1.2
        elif ghost_distance < 2.5:
            reward -= 0.5
        elif ghost_distance >= 3:
            reward += 1

        # Exploração de novas áreas
        if new_agent_pos_tuple not in self.visited_positions:
            reward += 2
            self.visited_positions.add(new_agent_pos_tuple)

        # Penalidade por repetir posições
        self.position_history.append(new_agent_pos_tuple)
        if self.position_history.count(new_agent_pos_tuple) > 3:
            reward -= 0.1

        # Penalidade por becos e bônus por áreas abertas
        if self._is_dead_end(new_agent_pos_tuple):
            reward -= 0.5
        elif self._is_open_area(new_agent_pos_tuple):
            reward += 1

        # Evitou rota prevista de fantasma
        if self.predicted_ghost_path and new_agent_pos_tuple not in self.predicted_ghost_path[:2]:
            reward += 1

        if ghost_abs is not None:
            new_ghost_distance = np.linalg.norm(new_agent_pos - ghost_abs)
            if new_ghost_distance > ghost_distance:
                reward += 0.5

        # Bónus final se apanhar todos os pellets
        if self.remaining_pellets == 0:
            reward += 200
            terminated = True

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
        
        # Primeiro, incrementa o contador de ações do agente
        if not hasattr(self, 'agent_steps'):
            self.agent_steps = 0
        self.agent_steps += 1

        # Update obstacle (ghost) positions without diagonal movement
        if self.agent_steps >= 50: #Os fantasmas só andam depois do agente fazer 50 ações
            for obstacle in self.obstacles:
                old_pos = obstacle.cur_pos

                #Determine a random direction for the ghost to move (up, down, left, or right)
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

        # If all pellets are collected, terminate the episode
        if self.n_pellets == 0:
            print(f"[ENV] All pellets collected! Cumulative Reward: {self.cumulative_reward}")
            self.close()

        # Update the mission text to reflect the new reward
        self.mission = f"Mode: {self.mode}      Episode: {self.current_episode}       Reward: {round(self.cumulative_reward,2)}        Pellets: {self.remaining_pellets}" \
            if self.mode == "Manual" else \
            f"Algorithm: {self.algorithm}       Episode: {self.current_episode}        Reward: {round(self.cumulative_reward,2)}        Pellets: {self.remaining_pellets}"

        return obs, reward, terminated, truncated, info

    def reset(self, seed=None, options=None):
        # Call the parent reset method which initializes everything
        obs, info = super().reset(seed=self.seed, options=options)

        # Create a list of available positions
        available_positions = [
            (x, y)
            for x in range(self.grid.width)
            for y in range(self.grid.height)
            if self.grid.get(x, y) is None
        ]

        # Filter out positions occupied by ghosts
        ghost_positions = {obstacle.cur_pos for obstacle in self.obstacles}
        available_positions = [
            pos for pos in available_positions if pos not in ghost_positions
        ]

        # Randomly select a new position for the agent from the available positions
        self.agent_pos = random.choice(available_positions)
        self.agent_dir = self.agent_start_dir
        self.cumulative_reward = 0
        self.remaining_pellets = self.n_pellets
        self.agent_steps = 0
        self.pellets_collected = 0
        self.ghost_hits = 0

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
            font = freetype.SysFont("Calibri", font_size)
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
