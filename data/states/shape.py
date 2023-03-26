import random

import pygame as pg
from pygame import Vector2

from data.colors import Colors

SHAPES = [
    [[True, True, True, True]],
    # [[False, True, False], [True, True, True]],
    # [[False, True, True], [True, True, False]],
    # [[True, True, False], [False, True, True]],
    # [[False, False, True], [True, True, True]],
    # [[True, False, False], [True, True, True]],
    # [[True, True], [True, True]],
]


class Shape:
    def __init__(self, color, size):
        self.shape = random.choice(SHAPES)
        self.color = color
        self.size = size
        self.position = pg.Vector2(2, 0)

    @property
    def width(self):
        return len(self.shape[0])

    @property
    def height(self):
        return len(self.shape)

    @property
    def coordinates(self):
        return self.get_coordinates()

    def get_coordinates(self, delta=Vector2(0, 0)):
        position = self.position + delta
        c = []
        for i in range(self.width):
            for j in range(self.height):
                if self.shape[j][i]:
                    v = Vector2((i + round(position.x), j + round(position.y)))
                    c.append(v)
        return c

    def rotate(self, horizontal_space, vertical_space, placed_elements):
        old_shape = self.shape.copy()
        if self.height <= horizontal_space and self.width <= vertical_space:
            self.shape = list(zip(*self.shape[::-1]))
            if self.check_collision(placed_elements, Vector2(0, 0)):
                self.shape = old_shape

    def move(self, delta):
        self.position += delta

    def check_collision(self, target_coordinates, delta):
        coordinates = self.get_coordinates(delta)
        for c in coordinates:
            if c in target_coordinates:
                return True
        return False

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
