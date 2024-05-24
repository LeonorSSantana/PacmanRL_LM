import pygame
from game.maze import Maze
from game.ghost import Ghost
from game.pacman import Pacman

class Game:
    def __init__(self, screen_height, header_height, footer_height):
        self.screen_height = screen_height
        self.header_height = header_height
        self.footer_height = footer_height
        self.cell_size = 20  # Adjusted size for smaller ghosts
        self.maze = Maze('assets/maze.txt', self.cell_size, screen_height, header_height, footer_height)
        start_x, start_y = self.maze.get_start_position()
        ghost_start_x, ghost_start_y = self.maze.get_ghost_start_position()
        self.pacman = Pacman(start_x, start_y, self.cell_size)
        self.ghosts = [
            Ghost('assets/images/ghosts/red.png', ghost_start_x, ghost_start_y, self.cell_size),
            Ghost('assets/images/ghosts/blue.png', ghost_start_x, ghost_start_y, self.cell_size),
            Ghost('assets/images/ghosts/pink.png', ghost_start_x, ghost_start_y, self.cell_size),
            Ghost('assets/images/ghosts/orange.png', ghost_start_x, ghost_start_y, self.cell_size)
        ]
        self.game_started = False

    def start_game(self):
        self.game_started = True

    def update(self, time_delta):
        self.pacman.update(self.maze, time_delta)
        for ghost in self.ghosts:
            ghost.update(self.maze, time_delta)

    def draw(self, screen):
        self.maze.draw(screen)
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.pacman.next_direction = (1, 0)
            elif event.key == pygame.K_LEFT:
                self.pacman.next_direction = (-1, 0)
            elif event.key == pygame.K_UP:
                self.pacman.next_direction = (0, -1)
            elif event.key == pygame.K_DOWN:
                self.pacman.next_direction = (0, 1)
