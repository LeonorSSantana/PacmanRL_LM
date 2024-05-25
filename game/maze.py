import pygame

class Maze:
    def __init__(self, level_data, cell_size, screen_height, header_height, footer_height):
        self.cell_size = cell_size
        self.screen_height = screen_height
        self.header_height = header_height
        self.footer_height = footer_height
        self.level_data = level_data
        self.grid_height = len(self.level_data)
        self.grid_width = len(self.level_data[0])
        self.maze_width = self.grid_width * self.cell_size
        self.maze_height = self.grid_height * self.cell_size
        self.offset_x = (pygame.display.get_surface().get_width() - self.maze_width) // 2
        self.offset_y = (self.screen_height - self.header_height - self.footer_height - self.maze_height) // 2 + self.header_height

    def draw(self, screen):
        num1 = self.cell_size
        num2 = self.cell_size
        math_pi = 3.141592653
        color = (0, 0, 139)
        for i in range(len(self.level_data)):
            for j in range(len(self.level_data[i])):
                x = j * num2 + self.offset_x
                y = i * num1 + self.offset_y
                if self.level_data[i][j] == 1:
                    pygame.draw.circle(screen, 'white', (x + (0.5 * num2), y + (0.5 * num1)), 4)
                if self.level_data[i][j] == 2:
                    pygame.draw.circle(screen, 'white', (x + (0.5 * num2), y + (0.5 * num1)), 10)
                if self.level_data[i][j] == 3:
                    pygame.draw.line(screen, color, (x + (0.5 * num2), y), (x + (0.5 * num2), y + num1), 3)
                if self.level_data[i][j] == 4:
                    pygame.draw.line(screen, color, (x, y + (0.5 * num1)), (x + num2, y + (0.5 * num1)), 3)
                if self.level_data[i][j] == 5:
                    pygame.draw.arc(screen, color, [(x - (num2 * 0.4)) - 2, (y + (0.5 * num1)), num2, num1], 0, math_pi / 2, 3)
                if self.level_data[i][j] == 6:
                    pygame.draw.arc(screen, color, [(x + (num2 * 0.5)), (y + (0.5 * num1)), num2, num1], math_pi / 2, math_pi, 3)
                if self.level_data[i][j] == 7:
                    pygame.draw.arc(screen, color, [(x + (num2 * 0.5)), (y - (0.4 * num1)), num2, num1], math_pi, 3 * math_pi / 2, 3)
                if self.level_data[i][j] == 8:
                    pygame.draw.arc(screen, color, [(x - (num2 * 0.4)) - 2, (y - (0.4 * num1)), num2, num1], 3 * math_pi / 2, 2 * math_pi, 3)
                if self.level_data[i][j] == 9:
                    pygame.draw.line(screen, 'white', (x, y + (0.5 * num1)), (x + num2, y + (0.5 * num1)), 3)
