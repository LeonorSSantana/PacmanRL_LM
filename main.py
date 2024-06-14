import pygame
from pygame_gui import UIManager
from gui.splash_screen import SplashScreen


def main():
    screen_width = 1280
    screen_height = 960

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PacmanRL: Reinforcement Learning for Pacman')
    manager = UIManager((screen_width, screen_height), 'gui/theme.json')
    manager.preload_fonts([{'name': 'Arial', 'point_size': 14, 'style': 'bold'}])
    clock = pygame.time.Clock()

    splash_screen = SplashScreen(screen, manager)

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            splash_screen.handle_events(event)
        splash_screen.draw()
        manager.update(time_delta)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
