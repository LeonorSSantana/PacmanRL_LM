# gui/options_window.py

import pygame
import pygame_gui
from pygame_gui.core import ObjectID


class OptionsWindow:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.window = None

        # Input fields
        self.n_ghosts_input = None
        self.n_pellets_input = None
        self.mode_dropdown = None
        self.speed_input = None
        self.deterministic_dropdown = None

        # Apply button
        self.apply_button = None

        # Default options
        self.n_ghosts = 4
        self.n_pellets = 30
        self.algorithm = 'Q-Learning'
        self.speed = 60  # FPS
        self.deterministic = True

    def show(self):
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect((320, 100), (640, 320)),
            manager=self.manager,
            window_display_title='Options',
            object_id=ObjectID('#options_window', class_id=None),
        )

        # Number of Ghosts
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 20), (200, 30)),
            text='Number of Ghosts:',
            manager=self.manager,
            container=self.window
        )
        self.n_ghosts_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, 20), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.n_ghosts_input.set_text(str(self.n_ghosts))

        # Number of Pellets
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 60), (200, 30)),
            text='Number of Pellets:',
            manager=self.manager,
            container=self.window
        )
        self.n_pellets_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, 60), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.n_pellets_input.set_text(str(self.n_pellets))

        # Algorithm (Q-Learning or SARSA)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 100), (200, 30)),
            text='Algorithm:',
            manager=self.manager,
            container=self.window
        )
        self.mode_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Q-Learning', 'SARSA'],
            starting_option=self.algorithm,
            relative_rect=pygame.Rect((220, 100), (200, 30)),
            manager=self.manager,
            container=self.window
        )

        # Speed (FPS)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 140), (200, 30)),
            text='Speed (FPS):',
            manager=self.manager,
            container=self.window
        )
        self.speed_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, 140), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.speed_input.set_text(str(self.speed))

        # Deterministic (Yes or No)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, 180), (200, 30)),
            text='Deterministic:',
            manager=self.manager,
            container=self.window
        )
        self.deterministic_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Yes', 'No'],
            starting_option='Yes' if self.deterministic else 'No',
            relative_rect=pygame.Rect((220, 180), (100, 30)),
            manager=self.manager,
            container=self.window
        )

        # Apply Button
        self.apply_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((270, 240), (100, 40)),
            text='Apply',
            manager=self.manager,
            container=self.window,
            object_id=ObjectID(class_id=None, object_id='#button_label'),
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element in [self.mode_dropdown, self.deterministic_dropdown]:
                if event.ui_element == self.mode_dropdown:
                    self.algorithm = self.mode_dropdown.selected_option[0]
                    print(f"[OPTIONS] Algorithm changed to: {self.algorithm}")
                elif event.ui_element == self.deterministic_dropdown:
                    self.deterministic = self.deterministic_dropdown.selected_option[0] == 'Yes'
                    print(f"[OPTIONS] Deterministic set to: {self.deterministic}")

            if event.type == pygame.QUIT or (event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == self.window):
                self.window.kill()

    def apply_settings(self):
        """
        Apply the current settings from the options window.
        """
        self.n_ghosts = int(self.n_ghosts_input.get_text())
        self.n_pellets = int(self.n_pellets_input.get_text())
        self.algorithm = self.mode_dropdown.selected_option[0]
        self.speed = int(self.speed_input.get_text())
        self.deterministic = self.deterministic_dropdown.selected_option[0] == 'Yes'

        return {
            'n_ghosts': self.n_ghosts,
            'n_pellets': self.n_pellets,
            'algorithm': self.algorithm,
            'speed': self.speed,
            'deterministic': self.deterministic
        }
