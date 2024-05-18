# gui/game_view.py
import pygame
import pygame_gui

from gui.footer_panel import FooterPanel
from gui.header_panel import HeaderPanel


class GameView:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.manager = pygame_gui.UIManager((800, 600))
        self.header_panel = HeaderPanel(self.manager, screen, game)
        self.footer_panel = FooterPanel(self.manager, screen)
        self.header_panel.create_ui_option_elements()
        self.footer_panel.create_battle_ui_elements()

    def render(self):
        self.screen.fill((0, 0, 0))
        self.game.render(self.screen)
        self.manager.draw_ui(self.screen)

    def update(self):
        self.game.update()
        self.footer_panel.update_stats(self.game.pacman.score, self.game.pacman.lives)
