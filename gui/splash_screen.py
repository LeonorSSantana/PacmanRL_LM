# gui/splash_screen.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from game.game import Game

LOGO_MARGIN_TOP = 240
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 60
BUTTON_POS_X = 540
BUTTON_POS_Y = 480


class SplashScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.logotype = None
        self.logotype_pos = None
        self.btn_about = None
        self.btn_options = None
        self.btn_play = None
        self.btn_exit = None
        self.start_game = False
        self.background_image = pygame.image.load('assets/images/bg-splash.png').convert()
        self.create_ui_elements()

    def create_ui_elements(self):
        self.logotype = pygame.image.load('assets/images/logo.png').convert_alpha()
        logotype_rect = self.logotype.get_rect(center=(self.screen.get_width() // 2, LOGO_MARGIN_TOP))
        self.logotype_pos = logotype_rect.topleft

        self.btn_play = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Play!',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_options = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Options',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_about = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING * 2), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='About',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING * 3), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Exit',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.screen.blit(self.logotype, self.logotype_pos)
        self.manager.draw_ui(self.screen)

    def handle_events(self, event):
        self.manager.process_events(event)
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.btn_play:
                    print("[SPLASH SCREEN] Starting game...")
                    self.start_game = True
                    game = Game()
                    game.start_game()
                elif event.ui_element == self.btn_options:
                    print("[SPLASH SCREEN] Options button pressed.")
                elif event.ui_element == self.btn_about:
                    print("[SPLASH SCREEN] About button pressed.")
                elif event.ui_element == self.btn_exit:
                    print("[SPLASH SCREEN] Exit button pressed.")
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
