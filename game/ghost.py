import pygame
import random
from game.pathfinding import a_star_pathfinding


class Ghost:
    def __init__(self, image_path, start_position, cell_size, ghost_id):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.center = start_position
        self.cell_size = cell_size
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # (dx, dy)
        self.speed = 2
        self.id = ghost_id
        self.dead = False

    def update(self, maze, time_delta, pacman_position):
        if not self.dead:
            path = a_star_pathfinding(self.rect.center, pacman_position, maze.level_data, maze.cell_size)
            if path:
                next_step = path[1]
                self.direction = (next_step[0] - self.rect.centerx) // self.cell_size, (
                            next_step[1] - self.rect.centery) // self.cell_size

        if self.can_move(maze, self.direction):
            self.rect.move_ip(self.speed * self.direction[0], self.speed * self.direction[1])

        self.align_to_grid()

    def can_move(self, maze, direction):
        next_rect = self.rect.move(self.speed * direction[0], self.speed * direction[1])
        for row_index, row in enumerate(maze.level_data):
            for col_index, cell in enumerate(row):
                if cell >= 3:  # Assuming 3 is the wall
                    wall_rect = pygame.Rect(
                        col_index * self.cell_size + maze.offset_x,
                        row_index * self.cell_size + maze.offset_y,
                        self.cell_size, self.cell_size)
                    if next_rect.colliderect(wall_rect):
                        return False
        return True

    def align_to_grid(self):
        if self.direction[0] != 0:
            self.rect.centery = round(self.rect.centery / self.cell_size) * self.cell_size
        if self.direction[1] != 0:
            self.rect.centerx = round(self.rect.centerx / self.cell_size) * self.cell_size

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def reset_position(self, position):
        self.rect.center = position
