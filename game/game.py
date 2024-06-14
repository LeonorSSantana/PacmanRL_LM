import pygame
import copy
from game.board import boards
from game.maze import Maze
from game.ghost import Ghost
from game.pacman import Pacman


class Game:
    def __init__(self, screen_height, header_height, footer_height):
        self.screen_height = screen_height
        self.header_height = header_height
        self.footer_height = footer_height

        self.game_started = False
        self.game_over = False
        self.game_won = False
        self.clock = pygame.time.Clock()

    def start_game(self):
        print("[GAME] Starting game...")
        self.game_started = True

    def update(self):
        if not self.game_started:
            return

    def draw(self, screen):
        pass

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                self.restart_game()

    def restart_game(self):
        print("[GAME] Restarting game...")
        self.game_started = False
        self.game_over = False
        self.game_won = False
