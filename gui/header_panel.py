# gui/header_panel.py
import pygame
import pygame_gui
from pygame_gui.core import ObjectID

class HeaderPanel(pygame_gui.elements.UIPanel):
    def __init__(self, manager, screen, game):
        margin_size_fixed = 5
        super().__init__(relative_rect=pygame.Rect(-margin_size_fixed, -margin_size_fixed,
                                                   screen.get_width() + margin_size_fixed * 2, 110),
                         starting_height=0,
                         manager=manager)
        self.manager = manager
        self.game = game
        self.screen = screen
        self.option_buttons = []
        self.option_buttons_size = 28

    def create_ui_option_elements(self):
        button_options = ['start', 'settings', 'log', 'exit']
        icons = [self.load_option_icon(option) for option in button_options]
        button_positions = self.calculate_button_positions(2, 2, self.option_buttons_size, self.option_buttons_size, 5, 35)

        self.option_buttons = []
        for i, icon in enumerate(icons):
            button = pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect(button_positions[i], (self.option_buttons_size, self.option_buttons_size)),
                text='',
                manager=self.manager,
                tool_tip_text=button_options[i].capitalize(),
                object_id=ObjectID(object_id=f"#{button_options[i]}_button", class_id="@icon_button"))
            self.option_buttons.append(button)

    def calculate_button_positions(self, rows, cols, button_width, button_height, padding, start_y):
        positions = []
        start_x = (self.relative_rect.width - (cols * button_width + (cols - 1) * padding)) // 2
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * (button_width + padding)
                y = start_y + row * (button_height + padding)
                positions.append((x, y))
        return positions

    @staticmethod
    def load_option_icon(icon_name):
        try:
            option_icon = pygame.image.load(f'assets/images/icons/{icon_name}.png').convert_alpha()
            return option_icon
        except FileNotFoundError as e:
            print(f"[SYSTEM] Error loading option icon {icon_name}: {e}")
            return None

    def destroy_ui_elements(self):
        for button in self.option_buttons:
            button.kill()
