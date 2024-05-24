import pygame
import random

class Ghost:
    def __init__(self, image_path, start_x, start_y, cell_size):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (cell_size, cell_size))
        self.rect = self.image.get_rect()
        self.rect.center = (start_x, start_y)
        self.cell_size = cell_size
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # (dx, dy)
        self.speed = cell_size // 4

    def update(self, maze, time_delta):
        if not self.can_move(maze, self.direction):
            self.direction = self.get_random_direction(maze)
        self.rect.move_ip(self.speed * self.direction[0], self.speed * self.direction[1])
        self.align_to_grid()

    def can_move(self, maze, direction):
        if direction == (0, 0):
            return False
        next_rect = self.rect.move(self.speed * direction[0], self.speed * direction[1])
        for row_index, row in enumerate(maze.level_data):
            for col_index, cell in enumerate(row):
                if cell >= 3:  # Assuming 3 and above are walls
                    wall_rect = pygame.Rect(
                        col_index * self.cell_size + maze.offset_x,
                        row_index * self.cell_size + maze.offset_y,
                        self.cell_size, self.cell_size)
                    if next_rect.colliderect(wall_rect):
                        return False
        return True

    def get_random_direction(self, maze):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for direction in directions:
            if self.can_move(maze, direction):
                self.direction = direction
                break
        return self.direction

    def align_to_grid(self):
        if self.direction[0] != 0:
            self.rect.centery = round(self.rect.centery / self.cell_size) * self.cell_size
        if self.direction[1] != 0:
            self.rect.centerx = round(self.rect.centerx / self.cell_size) * self.cell_size

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)
