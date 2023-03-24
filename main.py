import sys

import pygame as pg

from data.control import Control
from data.states.game import Game
from data.states.game_over import GameOverScreen
from data.states.start_menu import StartMenu

pg.init()
pg.display.set_caption("Tetris")

rows = 12
columns = 8
block_size = 60
top_bar_height = block_size
vertical_margin = 20
horizontal_margin = 20
side_bar_width = (4 * block_size) + (2 * horizontal_margin)
screen_height = (
    vertical_margin
    + top_bar_height
    + vertical_margin
    + (rows * block_size)
    + vertical_margin
)
screen_width = (
    horizontal_margin
    + (columns * block_size)
    + horizontal_margin
    + side_bar_width
    + horizontal_margin
)
size = (screen_width, screen_height)
fps = 1

app = Control(size, fps)
game = Game(
    rows,
    columns,
    block_size,
    top_bar_height,
    side_bar_width,
    vertical_margin,
    horizontal_margin,
)
state_dict = {
    "start": StartMenu(size),
    "game": game,
    "game_over": GameOverScreen(game),
}

app.setup_states(state_dict, "start")
app.game_loop()
pg.quit()
sys.exit()
