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
        self.cell_size = 20  # Adjusted size for the correct grid
        self.maze = Maze(boards, self.cell_size, screen_height, header_height, footer_height)
        self.level_data = copy.deepcopy(boards)

        self.pacman = Pacman(self.get_start_position(), self.cell_size)
        self.ghosts = [
            Ghost('assets/images/ghosts/red.png', self.get_ghost_start_position(), self.cell_size, 0),
            Ghost('assets/images/ghosts/blue.png', self.get_ghost_start_position(), self.cell_size, 1),
            Ghost('assets/images/ghosts/pink.png', self.get_ghost_start_position(), self.cell_size, 2),
            Ghost('assets/images/ghosts/orange.png', self.get_ghost_start_position(), self.cell_size, 3)
        ]

        self.game_started = False
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.game_won = False
        self.powerup = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.targets = [(0, 0), (0, 0), (0, 0), (0, 0)]
        self.moving = False
        self.startup_counter = 0
        self.direction_command = 0
        self.turns_allowed = [False, False, False, False]
        self.player_speed = 2
        self.clock = pygame.time.Clock()

    def get_start_position(self):
        x = self.maze.offset_x + self.cell_size * 14.5
        y = self.maze.offset_y + self.cell_size * 23
        return x, y

    def get_ghost_start_position(self):
        x = self.maze.offset_x + self.cell_size * 13.5
        y = self.maze.offset_y + self.cell_size * 17
        return x, y

    def start_game(self):
        self.game_started = True

    def update(self, time_delta):
        if not self.game_started:
            return

        self.handle_movement()
        self.check_collisions()

        for ghost in self.ghosts:
            ghost.update(self.maze, time_delta, self.pacman.get_center())

    def handle_movement(self):
        time_delta = self.clock.tick(60) / 1000.0
        center_x, center_y = self.pacman.get_center()
        self.turns_allowed = self.check_turns_allowed(center_x, center_y)

        if self.direction_command == 0 and self.turns_allowed[0]:
            self.pacman.set_direction(1, 0)
        elif self.direction_command == 1 and self.turns_allowed[1]:
            self.pacman.set_direction(-1, 0)
        elif self.direction_command == 2 and self.turns_allowed[2]:
            self.pacman.set_direction(0, -1)
        elif self.direction_command == 3 and self.turns_allowed[3]:
            self.pacman.set_direction(0, 1)

        self.pacman.update(self.maze, time_delta)

    def check_turns_allowed(self, center_x, center_y):
        turns = [False, False, False, False]
        num1 = (self.screen_height - 50) // 32
        num2 = pygame.display.get_surface().get_width() // 30

        if 0 < center_x < 870:
            if self.level_data[center_y // num1][center_x // num2] == 1:
                self.level_data[center_y // num1][center_x // num2] = 0
                self.score += 10
            if self.level_data[center_y // num1][center_x // num2] == 2:
                self.level_data[center_y // num1][center_x // num2] = 0
                self.score += 50
                self.powerup = True
                self.power_counter = 0
                self.eaten_ghost = [False, False, False, False]

        if self.level_data[center_y // num1][center_x // num2] < 3:
            turns[0] = True
        if self.level_data[center_y // num1][center_x // num2 - 1] < 3:
            turns[1] = True
        if self.level_data[center_y // num1 - 1][center_x // num2] < 3:
            turns[2] = True
        if self.level_data[center_y // num1 + 1][center_x // num2] < 3:
            turns[3] = True

        return turns

    def draw(self, screen):
        self.maze.draw(screen)
        self.pacman.draw(screen)
        for ghost in self.ghosts:
            ghost.draw(screen)
        self.draw_misc(screen)

    def draw_misc(self, screen):
        font = pygame.font.Font('freesansbold.ttf', 20)
        score_text = font.render(f'Score: {self.score}', True, 'white')
        screen.blit(score_text, (10, self.screen_height - 30))
        if self.powerup:
            pygame.draw.circle(screen, 'blue', (140, self.screen_height - 20), 15)
        for i in range(self.lives):
            screen.blit(pygame.transform.scale(self.pacman.images[0], (30, 30)),
                        (650 + i * 40, self.screen_height - 35))
        if self.game_over:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Game over! Space bar to restart!', True, 'red')
            screen.blit(gameover_text, (100, 300))
        if self.game_won:
            pygame.draw.rect(screen, 'white', [50, 200, 800, 300], 0, 10)
            pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
            gameover_text = font.render('Victory! Space bar to restart!', True, 'green')
            screen.blit(gameover_text, (100, 300))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.direction_command = 0
            if event.key == pygame.K_LEFT:
                self.direction_command = 1
            if event.key == pygame.K_UP:
                self.direction_command = 2
            if event.key == pygame.K_DOWN:
                self.direction_command = 3
            if event.key == pygame.K_SPACE and (self.game_over or self.game_won):
                self.restart_game()

    def restart_game(self):
        self.powerup = False
        self.power_counter = 0
        self.lives = 3
        self.startup_counter = 0
        self.pacman.reset_position(self.get_start_position())
        for ghost in self.ghosts:
            ghost.reset_position(self.get_ghost_start_position())
        self.eaten_ghost = [False, False, False, False]
        self.game_over = False
        self.game_won = False
        self.score = 0
        self.level_data = copy.deepcopy(boards)

    def check_collisions(self):
        center_x, center_y = self.pacman.get_center()
        player_circle = pygame.draw.circle(pygame.display.get_surface(), 'black', (center_x, center_y), 20, 2)

        if not self.powerup:
            for ghost in self.ghosts:
                if player_circle.colliderect(ghost.rect) and not ghost.dead:
                    if self.lives > 0:
                        self.lives -= 1
                        self.startup_counter = 0
                        self.pacman.reset_position(self.get_start_position())
                        for ghost2 in self.ghosts:
                            ghost2.reset_position(self.get_ghost_start_position())
                        self.eaten_ghost = [False, False, False, False]
                    else:
                        self.game_over = True
                        self.moving = False
                        self.startup_counter = 0
        else:
            for i, ghost in enumerate(self.ghosts):
                if player_circle.colliderect(ghost.rect) and not ghost.dead and not self.eaten_ghost[i]:
                    ghost.dead = True
                    self.eaten_ghost[i] = True
                    self.score += (2 ** self.eaten_ghost.count(True)) * 100
