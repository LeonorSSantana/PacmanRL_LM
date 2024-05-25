import pygame
from pygame_gui import UIManager
from game.view_controller import ViewController
from gui.game_view import GameView


def main():
    screen_width = 1280
    screen_height = 960

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('PacmanRL: Reinforcement Learning for Pacman')
    manager = UIManager((screen_width, screen_height), 'gui/theme.json')
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
        if view_controller.current_view and isinstance(view_controller.current_view, GameView) and view_controller.current_view.game_started:
            view_controller.current_view.game.update(time_delta)
        manager.update(time_delta)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
