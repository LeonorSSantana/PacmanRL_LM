from game.game import Game

class ViewController:
    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.current_view = None
        self.game = None

    def switch_to_splash_screen(self):
        from gui.splash_screen import SplashScreen
        if self.current_view:
            self.current_view.destroy_ui_elements()
        self.current_view = SplashScreen(self.screen, self.manager, self)
        self.current_view.create_ui_elements()

    def switch_to_game_view(self):
        from gui.game_view import GameView
        if self.current_view:
            self.current_view.destroy_ui_elements()
        screen_height = self.screen.get_height()
        header_height = 100  # Adjust as necessary
        footer_height = 100  # Adjust as necessary
        self.game = Game(screen_height, header_height, footer_height)
        self.current_view = GameView(self.screen, self.manager, self.game, self)
        self.current_view.create_ui_elements()

    def handle_events(self, event):
        if self.current_view:
            self.current_view.handle_events(event)

    def draw(self):
        if self.current_view:
            self.current_view.draw()
