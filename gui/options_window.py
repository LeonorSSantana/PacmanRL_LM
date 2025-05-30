import pygame
import pygame_gui
from pygame_gui.core import ObjectID

OPTION_WINDOW_SIZE = (640, 640)
OPTION_WINDOW_POS = (320, 100)

DEFAULT_SPACING = 40  # Default vertical spacing between elements


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

        # New options for RL training parameters
        self.num_episodes_input = None
        self.epsilon_input = None
        self.epsilon_decay_input = None
        self.learning_rate_input = None
        self.discount_factor_input = None

        # Apply button
        self.apply_button = None

        # Default options
        self.n_ghosts = 4
        self.n_pellets = 30
        self.algorithm = 'Q-Learning'
        self.speed = 60  # FPS
        self.deterministic = True
        self.num_episodes = 1000
        self.epsilon = 0.5
        self.epsilon_decay = 0.995
        self.learning_rate = 0.2
        self.discount_factor = 0.99  # Default discount factor

    def show(self):
        self.window = pygame_gui.elements.UIWindow(
            rect=pygame.Rect(OPTION_WINDOW_POS, OPTION_WINDOW_SIZE),
            manager=self.manager,
            window_display_title='Options',
            object_id=ObjectID('#options_window', class_id=None),
        )

        # Initial Y position
        current_y = 20

        # Section Label: Environment Settings
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Environment Settings',
            manager=self.manager,
            container=self.window
        )

        current_y += DEFAULT_SPACING

        # Number of Ghosts
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Number of Ghosts:',
            manager=self.manager,
            container=self.window
        )
        self.n_ghosts_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.n_ghosts_input.set_text(str(self.n_ghosts))

        current_y += DEFAULT_SPACING

        # Number of Pellets
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Number of Pellets:',
            manager=self.manager,
            container=self.window
        )
        self.n_pellets_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.n_pellets_input.set_text(str(self.n_pellets))

        current_y += DEFAULT_SPACING

        # Algorithm (Q-Learning or SARSA)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Algorithm:',
            manager=self.manager,
            container=self.window
        )
        self.mode_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Q-Learning', 'SARSA'],
            starting_option=self.algorithm,
            relative_rect=pygame.Rect((220, current_y), (200, 30)),
            manager=self.manager,
            container=self.window
        )

        current_y += DEFAULT_SPACING

        # Speed (FPS)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Speed (FPS):',
            manager=self.manager,
            container=self.window
        )
        self.speed_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.speed_input.set_text(str(self.speed))

        current_y += DEFAULT_SPACING

        # Deterministic (Yes or No)
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Deterministic:',
            manager=self.manager,
            container=self.window
        )
        self.deterministic_dropdown = pygame_gui.elements.UIDropDownMenu(
            options_list=['Yes', 'No'],
            starting_option='Yes' if self.deterministic else 'No',
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )

        current_y += DEFAULT_SPACING * 1.5  # Add extra space before the next section

        # Section Label: RL Settings
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='RL Settings',
            manager=self.manager,
            container=self.window
        )

        current_y += DEFAULT_SPACING

        # Number of Episodes
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Number of Episodes:',
            manager=self.manager,
            container=self.window
        )
        self.num_episodes_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.num_episodes_input.set_text(str(self.num_episodes))

        current_y += DEFAULT_SPACING

        # Epsilon Value
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Epsilon Value:',
            manager=self.manager,
            container=self.window
        )
        self.epsilon_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.epsilon_input.set_text(str(self.epsilon))

        current_y += DEFAULT_SPACING

        # Epsilon Decay
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Epsilon Decay:',
            manager=self.manager,
            container=self.window
        )
        self.epsilon_decay_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.epsilon_decay_input.set_text(str(self.epsilon_decay))

        current_y += DEFAULT_SPACING

        # Learning Rate
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Learning Rate:',
            manager=self.manager,
            container=self.window
        )
        self.learning_rate_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.learning_rate_input.set_text(str(self.learning_rate))

        current_y += DEFAULT_SPACING

        # Discount Factor
        pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((20, current_y), (200, 30)),
            text='Discount Factor:',
            manager=self.manager,
            container=self.window
        )
        self.discount_factor_input = pygame_gui.elements.UITextEntryLine(
            relative_rect=pygame.Rect((220, current_y), (100, 30)),
            manager=self.manager,
            container=self.window
        )
        self.discount_factor_input.set_text(str(self.discount_factor))

        current_y += DEFAULT_SPACING * 1.5

        # Apply Button
        self.apply_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((270, current_y), (100, 40)),
            text='Apply',
            manager=self.manager,
            container=self.window,
            object_id=ObjectID(class_id=None, object_id='#button_label'),
        )

    def handle_events(self, event):
        if event.type == pygame.USEREVENT:
            if (event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED
                    and event.ui_element in [self.mode_dropdown, self.deterministic_dropdown]):
                if event.ui_element == self.mode_dropdown:
                    self.algorithm = self.mode_dropdown.selected_option[0]
                    print(f"[OPTIONS] Algorithm changed to: {self.algorithm}")
                elif event.ui_element == self.deterministic_dropdown:
                    self.deterministic = self.deterministic_dropdown.selected_option[0] == 'Yes'
                    print(f"[OPTIONS] Deterministic set to: {self.deterministic}")

            if (event.type == pygame.QUIT
                    or (event.type == pygame_gui.UI_WINDOW_CLOSE and event.ui_element == self.window)):
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
        self.num_episodes = int(self.num_episodes_input.get_text())
        self.epsilon = float(self.epsilon_input.get_text())
        self.epsilon_decay = float(self.epsilon_decay_input.get_text())
        self.learning_rate = float(self.learning_rate_input.get_text())
        self.discount_factor = float(self.discount_factor_input.get_text())

        return {
            'n_ghosts': self.n_ghosts,
            'n_pellets': self.n_pellets,
            'algorithm': self.algorithm,
            'speed': self.speed,
            'deterministic': self.deterministic,
            'num_episodes': self.num_episodes,
            'epsilon': self.epsilon,
            'epsilon_decay': self.epsilon_decay,
            'learning_rate': self.learning_rate,
            'discount_factor': self.discount_factor
        }
