import os

import pygame

from data.colors import Colors
from data.states.base_state import BaseState


class StartMenu(BaseState):
    def __init__(self, size):
        BaseState.__init__(self)
        self.next = "game"
        self.screen_width, self.screen_height = size

    def get_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.switch_state()

    def update(self, screen):
        self.draw(screen)

    def draw(self, screen):
        screen.fill(Colors.BLACK)
        self.render_text(
            screen,
            "Tetris",
            Colors.WHITE,
            self.screen_width / 2,
            self.screen_height * 0.25,
            title=True,
        )
        self.render_text(
            screen,
            "Press space to start",
            Colors.WHITE,
            self.screen_width / 2,
            self.screen_height * 0.5,
        )
