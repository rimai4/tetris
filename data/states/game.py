import os
import random

import pygame as pg
from pygame.math import Vector2

from data.colors import Colors
from data.states.base_state import BaseState
from data.states.shape import SHAPES, Shape


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

        self.current_element = Shape(Colors.get_random_color(), self.block_size)
        self.placed_elements = []

        self.element_queue = [
            Shape(Colors.get_random_color(), self.block_size),
            Shape(Colors.get_random_color(), self.block_size),
            Shape(Colors.get_random_color(), self.block_size),
            Shape(Colors.get_random_color(), self.block_size),
        ]

        self.top_bar = pg.surface.Surface((self.main_screen_width, self.top_bar_height))
        self.main_screen = pg.surface.Surface(
            (self.main_screen_width, self.main_screen_height)
        )
        self.side_bar = pg.surface.Surface(
            (self.side_bar_width, self.main_screen_height)
        )

    def handle_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.current_element.rotate()
            if event.key == pg.K_DOWN:
                self.current_element.move(Vector2(0, 1))
                max_position = self.rows - self.current_element.vertical_element_count
                if self.current_element.position.y == max_position:
                    self.placed_elements.append(self.current_element)
                    self.current_element = self.element_queue.pop(0)
                    self.element_queue.append(
                        Shape(Colors.get_random_color(), self.block_size)
                    )
            if event.key == pg.K_LEFT:
                if self.current_element.position.x >= 1:
                    self.current_element.move(Vector2(-1, 0))
            if event.key == pg.K_RIGHT:
                max_position = (
                    self.columns - self.current_element.horizontal_element_count
                )
                if self.current_element.position.x < max_position:
                    self.current_element.move(Vector2(1, 0))

    def draw_placed_elements(self):
        for element in self.placed_elements:
            element.draw(
                self.main_screen,
                element.position.x * self.block_size,
                element.position.y * self.block_size,
            )

    def update(self, screen):
        screen.fill(Colors.BLACK)

        self.draw_top_bar()
        self.draw_main_screen()
        self.draw_side_bar()

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
        self.main_screen.fill(Colors.BLACK)
        rect = self.main_screen.get_rect()
        pg.draw.rect(self.main_screen, Colors.GREY, rect, width=2)

        self.current_element.draw(
            self.main_screen,
            self.current_element.position.x * self.block_size,
            self.current_element.position.y * self.block_size,
        )
        self.draw_placed_elements()

    def draw_side_bar(self):
        self.side_bar.fill(Colors.BLACK)
        rect = self.side_bar.get_rect()
        pg.draw.rect(self.side_bar, Colors.GREY, rect, width=2)
        for i, element in enumerate(self.element_queue):
            horizontal_margin = self.horizontal_margin
            if len(element.shape) < 4:
                horizontal_margin += len(element.shape) * (self.block_size / 2)
            element.draw(
                self.side_bar,
                horizontal_margin,
                self.vertical_margin * 2 + (i * self.block_size * 3),
            )
