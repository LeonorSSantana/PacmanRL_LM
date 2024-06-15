import sys

import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from game.game import Game
from gui.options_window import OptionsWindow

LOGO_MARGIN_TOP = 240
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_SPACING = 60
BUTTON_POS_X = 540
BUTTON_POS_Y = 420


class SplashScreen:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.logotype = None
        self.logotype_pos = None

        # Buttons
        self.btn_about = None
        self.btn_options = None
        self.btn_train_rl = None
        self.btn_test_rl = None
        self.btn_manual = None
        self.btn_exit = None

        # Window state
        self.options_window = None
        self.options_window_killed = True
        self.background_image = pygame.image.load('assets/images/bg-splash.png').convert()
        self.create_ui_elements()

        # Game settings
        self.game_is_running = False
        self.game_settings = None

    def create_ui_elements(self):
        self.logotype = pygame.image.load('assets/images/logo.png').convert_alpha()
        logotype_rect = self.logotype.get_rect(center=(self.screen.get_width() // 2, LOGO_MARGIN_TOP))
        self.logotype_pos = logotype_rect.topleft

        self.btn_train_rl = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Train RL',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_test_rl = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Test RL',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_manual = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING * 2), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Manual Mode',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_options = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING * 3), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='Options',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_about = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING * 4), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text='About',
            manager=self.manager,
            object_id=ObjectID(class_id=None, object_id='#button-label'),
        )
        self.btn_exit = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((BUTTON_POS_X, BUTTON_POS_Y + BUTTON_SPACING * 5), (BUTTON_WIDTH, BUTTON_HEIGHT)),
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

        if self.options_window and not self.options_window_killed:
            # If options window is visible, pass events to it
            self.options_window.handle_events(event)
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.options_window.apply_button:
                    # Retrieve settings from the options window
                    settings = self.options_window.apply_settings()
                    print("[SPLASH SCREEN] Settings applied:", settings)

                    # Apply settings to the game instance
                    self.game_settings = settings

                    # Close the options window
                    self.options_window.window.kill()
                    self.options_window_killed = True
                    self.options_window = None
        elif not self.game_is_running:
            # Handle splash screen events
            if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.btn_train_rl:
                    print("[SPLASH SCREEN] Training RL...")
                    self.start_game('Training')
                elif event.ui_element == self.btn_test_rl:
                    print("[SPLASH SCREEN] Testing RL...")
                    self.start_game('Testing')
                elif event.ui_element == self.btn_manual:
                    print("[SPLASH SCREEN] Manual Mode")
                    self.start_game('Manual')
                elif event.ui_element == self.btn_options:
                    if self.options_window is None or self.options_window_killed:
                        print("[SPLASH SCREEN] Options window opened.")
                        self.options_window = OptionsWindow(self.screen, self.manager)
                        self.options_window_killed = False
                        self.options_window.show()
                elif event.ui_element == self.btn_about:
                    print("[SPLASH SCREEN] About button pressed.")
                elif event.ui_element == self.btn_exit:
                    print("[SPLASH SCREEN] Exit button pressed.")
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        # Verify if the options window was closed
        if event.type == pygame_gui.UI_WINDOW_CLOSE and self.options_window and event.ui_element == self.options_window.window:
            print("[SPLASH SCREEN] Options window closed.")
            self.options_window_killed = True
            self.options_window = None

    def start_game(self, mode):
        """
        Start the game with the specified mode.
        """
        self.game_is_running = True
        settings = self.game_settings if self.game_settings else {}
        settings['mode'] = mode
        settings['algorithm'] = 'Q-Learning' if settings.get('algorithm') is None else settings['algorithm']

        # Clean up before starting the game
        pygame.quit()

        game = Game()
        game.start_game(**settings)

        print(f"[SPLASH SCREEN] {mode} session finished.")
        self.exit_game()

    def exit_game(self):
        """
        Exit the game and return to the splash screen.
        """
        self.game_is_running = False
        pygame.quit()
        sys.exit(0)
