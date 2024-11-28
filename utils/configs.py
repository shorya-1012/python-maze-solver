import pygame

pygame.init()
pygame.font.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (208, 240, 192)
SKY_BLUE = (135, 206, 235)

MAX_FPS = 240

WIDTH = 800
HEIGHT = 900

TOOLBAR_HEIGHT = HEIGHT - WIDTH

ROWS = COLS = 50

PIXEL_SIZE = WIDTH // COLS

BG_COLOR = WHITE


def get_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont("comicsans", size)
