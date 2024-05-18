# view_controller.py
from game.game import Game


class ViewController:
    """Class to manage the views and switch between them.
    :param screen: Pygame screen object to draw on
    :param manager: Pygame GUI manager object to manage UI elements
    :var current_view: Current view being displayed
    :var game: Game object containing the current game state
    """

    def __init__(self, screen, manager):
        self.screen = screen
        self.manager = manager
        self.current_view = None
        self.game = None

    def switch_to_splash_screen(self):
        """Switch to the splash screen view."""
        from gui.splash_screen import SplashScreen
        if self.current_view:
            self.current_view.destroy_ui_elements()
        self.current_view = SplashScreen(self.screen, self.manager, self)
        self.current_view.create_ui_elements()

    def switch_to_game_view(self):
        """Switch to the game view."""
        from gui.game_view import GameView
        if self.current_view:
            self.current_view.destroy_ui_elements()
        # Initialize or reset the game state as necessary
        if self.game:
            del self.game
        self.game = Game()
        self.current_view = GameView(self.screen, self.manager, self.game, self)
        self.current_view.create_ui_elements()

    def handle_events(self, event):
        """Handle events for the current view."""
        if self.current_view:
            self.current_view.handle_events(event)

    def draw(self):
        """Draw the current view."""
        if self.current_view:
            self.current_view.draw()
