import pygame

class Pacman:
    def __init__(self, start_x, start_y, cell_size):
        self.images = [pygame.transform.scale(pygame.image.load(f'assets/images/pacman/{i}.png'), (cell_size, cell_size)) for i in range(1, 5)]
        self.rect = self.images[0].get_rect()
        self.rect.center = (start_x, start_y)
        self.cell_size = cell_size
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = cell_size // 4
        self.image_index = 0
        self.animation_counter = 0

    def update(self, maze, time_delta):
        if self.can_move(maze, self.next_direction):
            self.direction = self.next_direction

        if self.can_move(maze, self.direction):
            self.rect.move_ip(self.speed * self.direction[0], self.speed * self.direction[1])

        self.align_to_grid()
        self.animate()

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

    def align_to_grid(self):
        if self.direction[0] != 0:
            self.rect.centery = round(self.rect.centery / self.cell_size) * self.cell_size
        if self.direction[1] != 0:
            self.rect.centerx = round(self.rect.centerx / self.cell_size) * self.cell_size

    def animate(self):
        self.animation_counter += 1
        if self.animation_counter >= 10:
            self.animation_counter = 0
            self.image_index = (self.image_index + 1) % len(self.images)

    def draw(self, screen):
        screen.blit(self.images[self.image_index], self.rect.topleft)
