# main.py
import pygame
from pygame_gui import UIManager
from game.view_controller import ViewController


def main():
    """
    Main function to run the game.
    Initializes Pygame, creates the screen and GUI manager, and starts the main game loop.
    """
    screen_width = 1280
    screen_height = 960

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PacmanRL: Reinforcement Learning in the World of Pacman')
    manager = UIManager((screen_width, screen_height), 'gui/theme.json')
    # Preload the Fira Code font for use in the game
    manager.preload_fonts([{'name': 'fira_code', 'point_size': 14, 'style': 'bold'}])
    clock = pygame.time.Clock()

    view_controller = ViewController(screen, manager)

    view_controller.switch_to_splash_screen()

    running = True
    while running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            view_controller.handle_events(event)

        view_controller.draw()
        manager.update(time_delta)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
