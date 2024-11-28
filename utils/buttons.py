import pygame
from .configs import BLACK, get_font


class Button:
    def __init__(self, x, y, width, height, color, text, text_color=BLACK) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, win: pygame.Surface):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2)
        button_font = get_font(20)
        text_surface = button_font.render(self.text, 1, self.text_color)
        win.blit(
            text_surface,
            (
                self.x + self.width / 2 - text_surface.get_width() / 2,
                self.y + self.height / 2 - text_surface.get_height() / 2,
            ),
        )

    def clicked(self, mouse_pos) -> bool:
        xcor, ycor = mouse_pos

        if not (xcor >= self.x and xcor <= self.x + self.width):
            return False
        if not (ycor >= self.y and ycor <= self.y + self.height):
            return False
        return True
