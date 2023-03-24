import random


class Colors:
    BLACK = (0, 0, 0)
    GREY = (127, 132, 144)
    WHITE = (255, 255, 255)
    BLUE = (118, 204, 224)
    ORANGE = (243, 150, 96)
    RED = (252, 93, 124)
    GREEN = (158, 208, 114)
    YELLOW = (231, 198, 100)

    BLOCK_COLORS = [
        BLUE,
        ORANGE,
        RED,
        GREEN,
        YELLOW,
    ]

    @staticmethod
    def get_random_color():
        return random.choice(Colors.BLOCK_COLORS)
