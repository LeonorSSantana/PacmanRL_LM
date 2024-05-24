import pygame
import pygame_gui
from gui.footer_panel import FooterPanel
from gui.header_panel import HeaderPanel


class GameView:
    def __init__(self, screen, manager, game, view_controller=None):
        self.screen = screen
        self.manager = manager
        self.game = game
        self.view_controller = view_controller
        self.background_image = pygame.image.load('assets/images/bg.png').convert()
        self.header_panel = None
        self.footer_panel = None
        self.game_started = False

    def create_ui_elements(self):
        self.header_panel = HeaderPanel(manager=self.manager, screen=self.screen, game=self.game)
        self.header_panel.create_ui_option_elements()
        self.footer_panel = FooterPanel(manager=self.manager, screen=self.screen)

    def destroy_ui_elements(self):
        self.header_panel.destroy_ui_elements()
        self.footer_panel.destroy_ui_elements()
        self.header_panel.kill()
        self.footer_panel.kill()

    def handle_events(self, event):
        self.manager.process_events(event)
        if event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element in self.header_panel.option_buttons:
                if event.ui_element.object_ids[0] == '#start_button':
                    self.start_game()
                elif event.ui_element.object_ids[0] == '#settings_button':
                    print("[GAME_VIEW] Configuration window opened...")
                elif event.ui_element.object_ids[0] == '#log_button':
                    self.open_log_window()
                elif event.ui_element.object_ids[0] == '#exit_button':
                    print("[GAME_VIEW] Switching to splash screen...")
                    self.game_started = False
                    self.view_controller.switch_to_splash_screen()
        elif event.type == pygame.KEYDOWN:
            self.game.handle_events(event)

    def open_log_window(self):
        print("[GAME_VIEW] Log window opened...")
        window_rect = pygame.Rect(0, 0, 800, 600)
        window_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        window_title = "Game Log"
        log_console_window = pygame_gui.elements.UIWindow(
            rect=window_rect,
            manager=self.manager,
            window_display_title=window_title,
            object_id="#log_console_window"
        )

    def start_game(self):
        self.game_started = True

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        self.manager.draw_ui(self.screen)
        if self.game_started:
            self.game.draw(self.screen)
