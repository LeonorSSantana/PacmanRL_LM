import sys
import pygame
from agents.q_learning import QLearning
from agents.sarsa import SARSA
from .environment import PacmanEnv
from minigrid.manual_control import ManualControl


class Game:
    def __init__(self):
        self.game_settings = None
        self.game_started = False
        self.env = None

        # Default game settings
        self.default_settings = {
            'grid_size': 24,
            'n_ghosts': 4,
            'n_pellets': 30,
            'mode': 'Manual',
            'algorithm': None,  # None means no specific algorithm chosen
            'speed': 60,  # Frames per second
            'deterministic': True,
            'epsilon': 1.0,
            'epsilon_decay': 0.995,
            'min_epsilon' : 0.05,
            'discount_factor': 0.9,
            'learning_rate': 0.2,
            'num_episodes': 1000
        }

        self.clock = pygame.time.Clock()

    def start_game(self, **kwargs):
        # Apply settings, using defaults for any missing values
        self.game_settings = {**self.default_settings, **kwargs}

        print(f"[GAME] Environment Settings:\n"
              f"-> Ghosts={self.game_settings['n_ghosts']}\n"
              f"-> Pellets={self.game_settings['n_pellets']}\n"
              f"-> Mode={self.game_settings['mode']}\n"
              f"-> Algorithm={self.game_settings['algorithm']}\n"
              f"-> Speed={self.game_settings['speed']}\n"
              f"-> Deterministic={self.game_settings['deterministic']}")

        print(f"[GAME] RL Settings:\n"
              f"-> Num Episodes={self.game_settings['num_episodes']}\n"
              f"-> Epsilon={self.game_settings['epsilon']}\n"
              f"-> Epsilon Decay={self.game_settings['epsilon_decay']}\n"
              f"-> Discount Factor={self.game_settings['discount_factor']}\n"
              f"-> Learning Rate={self.game_settings['learning_rate']}\n")

        # Close the current Pygame window if open
        pygame.quit()

        # Initialize a new Pygame window
        pygame.init()
        pygame.display.set_mode((900, 900))

        # Initialize the Pacman Minigrid environment
        self.env = PacmanEnv(
            grid_size=self.game_settings['grid_size'],
            n_ghosts=self.game_settings['n_ghosts'],
            n_pellets=self.game_settings['n_pellets'],
            mode=self.game_settings['mode'],
            algorithm=self.game_settings['algorithm'],
            frames_per_second=self.game_settings['speed'],
            seed=1 if self.game_settings['deterministic'] else None
        )
        print("Action Space:", self.env.action_space)

        # Start the game in Manual mode
        if self.game_settings['mode'] == "Manual":
            manual_control = ManualControl(self.env)
            manual_control.start()

        # Start the game in Training mode
        if self.game_settings['mode'] == "Training":
            if self.game_settings['algorithm'] == 'Q-Learning':
                print("[GAME] Training Q-Learning agent...")
                q_learning_agent = QLearning(
                    self.env,
                    epsilon=self.game_settings['epsilon'],
                    epsilon_decay=self.game_settings['epsilon_decay'],
                    gamma=self.game_settings['discount_factor'],
                    alpha=self.game_settings['learning_rate']
                )
                q_learning_agent.train(num_episodes=self.game_settings['num_episodes'])
                q_learning_agent.save_q_table(filename='models/q_learning_solution.pkl')
                self.game_started = False
            elif self.game_settings['algorithm'] == 'SARSA':
                print("[GAME] Training SARSA agent...")
                sarsa_agent = SARSA(
                    self.env,
                    epsilon=self.game_settings['epsilon'],
                    epsilon_decay=self.game_settings['epsilon_decay'],
                    gamma=self.game_settings['discount_factor'],
                    alpha=self.game_settings['learning_rate']
                )
                sarsa_agent.train(num_episodes=self.game_settings['num_episodes'])
                sarsa_agent.save_q_table(filename='models/sarsa_solution.pkl')
                self.game_started = False

        # Start the game in Testing mode
        elif self.game_settings['mode'] == "Testing":
            if self.game_settings['algorithm'] == 'Q-Learning':
                print("[GAME] Testing Q-Learning agent...")
                q_learning_agent = QLearning(self.env)
                q_learning_agent.load_q_table(filename='models/q_learning_solution.pkl')
                q_learning_agent.test(num_episodes=100)
            elif self.game_settings['algorithm'] == 'SARSA':
                print("[GAME] Testing SARSA agent...")
                sarsa_agent = SARSA(self.env)
                sarsa_agent.load_q_table(filename='models/sarsa_solution.pkl')
                sarsa_agent.test(num_episodes=100)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game_started = False
                pygame.quit()
                sys.exit()
