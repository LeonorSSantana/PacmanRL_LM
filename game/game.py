# game/game.py
from game.pacman import PacMan
from game.ghost import Ghost
from game.maze import Maze


class Game:
    def __init__(self):
        self.maze = Maze('assets/maze.png')
        self.pacman = PacMan(100, 100)
        self.ghosts = [Ghost(200, 200), Ghost(300, 300)]
        # TODO: Add other game elements like pellets

    def update(self):
        self.pacman.update(self.maze)
        for ghost in self.ghosts:
            ghost.update(self.maze)

    def render(self, screen):
        self.maze.render(screen)
        self.pacman.render(screen)
        for ghost in self.ghosts:
            ghost.render(screen)
