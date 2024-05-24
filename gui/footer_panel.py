import pygame_gui
import pygame


class FooterPanel(pygame_gui.elements.UIPanel):
    def __init__(self, manager, screen):
        self.margin_size_fixed = 5
        super().__init__(relative_rect=pygame.Rect(-self.margin_size_fixed, screen.get_height() - 105,
                                                   screen.get_width() + self.margin_size_fixed * 2, 110),
                         starting_height=0,
                         manager=manager)
        self.manager = manager
        self.screen = screen
        self.stats_label = None

    def create_maze_ui_elements(self):
        self.stats_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect(10, 10, 400, 30),
            text="",
            manager=self.manager
        )

    def update_stats(self, score, lives, q_learning_rewards):
        self.stats_label.set_text(f"Score: {score} | Lives: {lives} | Q-Learning Rewards: {q_learning_rewards}")

    def destroy_ui_elements(self):
        if self.stats_label:
            self.stats_label.kill()
