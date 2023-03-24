import pygame

from data.colors import Colors
from data.states.base_state import BaseState


class GameOverScreen(BaseState):
    def __init__(self, game):
        BaseState.__init__(self)
        self.next = "game"
        self.game = game
        self.high_scores = []

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def update(self, screen):
        self.draw(screen)

    def draw(self, screen):
        size = self.game.game_screen_size
        screen.fill(Colors.BLACK)
        self.render_text(
            screen, "Game over", Colors.WHITE, size / 2, size * 0.15, title=True
        )
