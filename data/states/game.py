import os
import random

import pygame as pg

from data.colors import Colors
from data.states.base_state import BaseState


class Game(BaseState):
    def __init__(
        self,
        rows,
        columns,
        block_size,
        top_bar_height,
        side_bar_width,
        vertical_margin,
        horizontal_margin,
    ):
        BaseState.__init__(self)
        self.rows = rows
        self.columns = columns
        self.block_size = block_size
        self.top_bar_height = top_bar_height
        self.side_bar_width = side_bar_width
        self.vertical_margin = vertical_margin
        self.horizontal_margin = horizontal_margin
        self.main_screen_width = columns * block_size
        self.main_screen_height = rows * block_size

        self.top_bar = pg.surface.Surface((self.main_screen_width, self.top_bar_height))
        self.main_screen = pg.surface.Surface(
            (self.main_screen_width, self.main_screen_height)
        )
        self.side_bar = pg.surface.Surface(
            (self.side_bar_width, self.main_screen_height)
        )

    def update(self, screen):
        self.draw_top_bar()
        self.draw_main_screen()
        self.draw_side_bar()

        screen.fill(Colors.BLACK)
        screen.blit(self.top_bar, (self.horizontal_margin, self.vertical_margin))
        screen.blit(
            self.main_screen,
            (
                self.horizontal_margin,
                self.vertical_margin + self.top_bar_height + self.vertical_margin,
            ),
        )
        screen.blit(
            self.side_bar,
            (
                self.horizontal_margin
                + self.main_screen_width
                + self.horizontal_margin,
                self.vertical_margin + self.top_bar_height + self.vertical_margin,
            ),
        )

    def draw_top_bar(self):
        rect = self.top_bar.get_rect()
        pg.draw.rect(self.top_bar, Colors.GREY, rect, width=2)

    def draw_main_screen(self):
        rect = self.main_screen.get_rect()
        pg.draw.rect(self.main_screen, Colors.GREY, rect, width=2)

    def draw_side_bar(self):
        rect = self.side_bar.get_rect()
        pg.draw.rect(self.side_bar, Colors.GREY, rect, width=2)

    def draw_bordered_rect(self, surface, x, y, width, height, color):
        rect = pg.rect.Rect(x, y, width, height)
        rect2 = pg.rect.Rect(x, y, width, height)
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, Colors.GREY, rect2, width=2)
