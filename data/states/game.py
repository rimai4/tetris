import random
from collections import namedtuple

import pygame as pg
from pygame import Vector2

from data.colors import Colors
from data.states.base_state import BaseState
from data.states.events import MOVE_MAIN_ELEMENT
from data.states.shape import Shape

PlacedBlock = namedtuple("PlacedBlock", ["position", "color"])


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
        self.placed_blocks = []

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

    @property
    def placed_coordinates(self):
        return list(map(lambda x: x.position, self.placed_blocks))

    def setup(self):
        pg.time.set_timer(MOVE_MAIN_ELEMENT, 700)

    def place_current_element(self):
        self.add_placed_blocks()
        self.current_element = self.element_queue.pop(0)
        self.element_queue.append(Shape(Colors.get_random_color(), self.block_size))

    def add_placed_blocks(self):
        coordinates = self.current_element.get_coordinates()
        for c in coordinates:
            placed_block = PlacedBlock(c, self.current_element.color)
            self.placed_blocks.append(placed_block)

    def draw_placed_blocks(self):
        for block in self.placed_blocks:
            self.draw_placed_block(block)

    def draw_placed_block(self, block):
        rect = pg.rect.Rect(
            block.position.x * self.block_size,
            block.position.y * self.block_size,
            self.block_size,
            self.block_size,
        )
        pg.draw.rect(self.main_screen, block.color, rect)
        pg.draw.rect(self.main_screen, Colors.GREY, rect, width=2)

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

    def move_down(self):
        bottom_reached = (
            self.rows - self.current_element.height == self.current_element.position.y
        )
        collision = self.current_element.check_collision(
            self.placed_coordinates, Vector2(0, 1)
        )

        if bottom_reached or collision:
            self.place_current_element()
        else:
            self.current_element.move(Vector2(0, 1))

    def move_left(self):
        if (
            self.current_element.position.x >= 1
            and not self.current_element.check_collision(
                self.placed_coordinates, Vector2(-1, 0)
            )
        ):
            self.current_element.move(Vector2(-1, 0))

    def move_right(self):
        max_position = self.columns - self.current_element.width
        if (
            self.current_element.position.x < max_position
            and not self.current_element.check_collision(
                self.placed_coordinates, Vector2(1, 0)
            )
        ):
            self.current_element.move(Vector2(1, 0))

    def handle_event(self, event):
        if event.type == MOVE_MAIN_ELEMENT:
            self.move_down()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                horizontal_space = self.columns - self.current_element.position.x
                vertical_space = self.rows - self.current_element.position.y
                self.current_element.rotate(
                    horizontal_space, vertical_space, self.placed_coordinates
                )
            if event.key == pg.K_DOWN:
                self.move_down()

            if event.key == pg.K_LEFT:
                self.move_left()
            if event.key == pg.K_RIGHT:
                self.move_right()

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
        self.draw_placed_blocks()

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
