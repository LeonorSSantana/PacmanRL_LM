import sys

import pygame

from agents.q_learning import QLearning
from .environment import PacmanEnv
from minigrid.manual_control import ManualControl


class Game:
    def __init__(self):
        self.game_started = False
        self.clock = pygame.time.Clock()

    def start_game(self):
        print("[GAME] Starting game...")
        self.game_started = True

        # Close the current Pygame window
        pygame.quit()

        # Initialize a new Pygame window
        pygame.init()
        pygame.display.set_mode((640, 640))

        # Initialize the Pacman Minigrid environment
        grid_size = 24
        n_ghosts = 8
        n_pellets = 15
        mode = "Q-Learning"  # "Manual", "Q-Learning" or "SARSA"
        speed = 30  # Number of frames per second for rendering
        env = PacmanEnv(grid_size=24, n_ghosts=n_ghosts, n_pellets=n_pellets, mode=mode, frames_per_second=speed)

        # Create QLearning agent
        q_learning_agent = QLearning(env)
        q_learning_agent.train(num_episodes=1000)
        q_learning_agent.save_q_table()

        # Enable manual control for testing
        # manual_control = ManualControl(env)
        # manual_control.start()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_started = False
                pygame.quit()
                sys.exit()
