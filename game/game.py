import pygame
from .environment import PacmanEnv
from minigrid.manual_control import ManualControl


class Game:
    def __init__(self):
        self.game_started = False
        self.game_over = False
        self.game_won = False
        self.clock = pygame.time.Clock()

    def start_game(self):
        print("[GAME] Starting game...")
        self.game_started = True

        # Close the current Pygame window
        pygame.display.quit()

        # Initialize a new Pygame window
        pygame.display.init()
        pygame.display.set_mode((640, 640))

        # Initialize the Pacman Minigrid environment
        grid_size = 24
        n_ghosts = 8
        n_pellets = 15
        env = PacmanEnv(grid_size=24, n_ghosts=n_ghosts, n_pellets=n_pellets)

        # Enable manual control for testing
        manual_control = ManualControl(env)
        manual_control.start()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.restart_game()

    def restart_game(self):
        print("[GAME] Restarting game...")
        self.game_over = False
        self.game_won = False
