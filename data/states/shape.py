import random

import pygame as pg

from data.colors import Colors

SHAPES = [
    [[True, True, True, True]],
    [[False, True, False], [True, True, True]],
    [[False, True, True], [True, True, False]],
    [[True, True, False], [False, True, True]],
    [[False, False, True], [True, True, True]],
    [[True, False, False], [True, True, True]],
    [[True, True], [True, True]],
]


class Shape:
    def __init__(self, color, size):
        self.shape = random.choice(SHAPES)
        self.color = color
        self.size = size
        self.position = pg.Vector2(2, 0)

    @property
    def vertical_element_count(self):
        return len(self.shape)

    @property
    def horizontal_element_count(self):
        return len(self.shape[0])

    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))

    def move(self, delta):
        self.position += delta

    def draw(self, surface, start_x, start_y):
        for j, row in enumerate(self.shape):
            for i, block in enumerate(row):
                if block:
                    rect = pg.rect.Rect(
                        start_x + (i * self.size),
                        start_y + (j * self.size),
                        self.size,
                        self.size,
                    )
                    pg.draw.rect(surface, self.color, rect)
                    pg.draw.rect(surface, Colors.GREY, rect, width=2)
