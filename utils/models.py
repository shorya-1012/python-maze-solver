from .configs import WHITE, BLACK


class GridPixel:
    def __init__(self, color=WHITE) -> None:
        self.is_blocked = False
        self.color = color

    def block_pixel(self) -> None:
        self.is_blocked = True
        self.color = BLACK
