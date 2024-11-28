from collections import deque
from utils import *
import time
import heapq

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver")
PATH_FOUND = False
START = (0, 0)
END = (ROWS - 1, COLS - 1)

BUTTON_Y = HEIGHT - TOOLBAR_HEIGHT + 25
BUTTONS = [
    Button(10, BUTTON_Y, 130, 50, (255, 69, 0), "SOLVE WITH A*", WHITE),
    Button(150, BUTTON_Y, 130, 50, (30, 144, 255), "SOLVE WITH BFS", WHITE),
    Button(290, BUTTON_Y, 70, 50, (50, 205, 50), "START"),
    Button(370, BUTTON_Y, 70, 50, (255, 215, 0), "END"),
    Button(450, BUTTON_Y, 70, 50, (135, 206, 235), "REDO"),
    Button(530, BUTTON_Y, 70, 50, (220, 20, 60), "CLEAR"),
]


# A*
def a_star(grid: list[list[GridPixel]], start, end):
    def is_valid_move(row, col) -> bool:
        if (
            row >= 0
            and col >= 0
            and row < len(grid)
            and col < len(grid[0])
            and not grid[row][col].is_blocked
        ):
            return True
        return False

    def get_h_distance(start, end):
        x1, y1 = start
        x2, y2 = end

        return abs(x1 - x2) + abs(y1 - y2)

    path = []

    drow = [0, 0, 1, -1]
    dcol = [1, -1, 0, 0]

    pq = []
    parent_node = {}
    g_cost = {}
    initial_h = get_h_distance(start, end)

    parent_node[start] = None
    g_cost[start] = 0
    heapq.heappush(pq, (initial_h, start[0], start[1]))

    while pq:
        _, curr_row, curr_col = heapq.heappop(pq)
        if (curr_row, curr_col) == end:
            while parent_node[(curr_row, curr_col)] is not None:
                path.append((curr_row, curr_col))
                curr_row, curr_col = parent_node[(curr_row, curr_col)]
            return path
        for i in range(len(drow)):
            new_row = curr_row + drow[i]
            new_col = curr_col + dcol[i]

            if is_valid_move(new_row, new_col):
                new_g_cost = g_cost[(curr_row, curr_col)] + 1
                if (new_row, new_col) not in g_cost or g_cost[
                    (new_row, new_col)
                ] > new_g_cost:
                    new_h_distance = get_h_distance((new_row, new_col), end)
                    new_f_distance = new_g_cost + new_h_distance
                    heapq.heappush(pq, (new_f_distance, new_row, new_col))
                    g_cost[(new_row, new_col)] = new_g_cost
                    parent_node[(new_row, new_col)] = (curr_row, curr_col)
                    grid[new_row][new_col].color = GREEN
                    draw(WIN, grid, BUTTONS)
                    time.sleep(0.001)

    return path


# bfs
def bfs(grid: list[list[GridPixel]], start, end):
    def is_valid_move(row, col, visited) -> bool:
        if (
            row >= 0
            and col >= 0
            and row < len(grid)
            and col < len(grid[0])
            and (row, col) not in visited
            and not grid[row][col].is_blocked
        ):
            return True

        return False

    queue = deque()
    queue.append(start)

    visited = {start: start}
    path = []

    drow = [1, -1, 0, 0]
    dcol = [0, 0, 1, -1]

    while queue:
        curr_row, curr_col = queue.popleft()

        if (curr_row, curr_col) == end:
            check_node = (curr_row, curr_col)
            while visited[check_node] != check_node:
                path.append(check_node)
                check_node = visited[check_node]
            return path

        for i in range(len(drow)):
            new_row = curr_row + drow[i]
            new_col = curr_col + dcol[i]

            if is_valid_move(new_row, new_col, visited):
                queue.append((new_row, new_col))
                visited[(new_row, new_col)] = (curr_row, curr_col)
                grid[new_row][new_col].color = GREEN
                draw(WIN, grid, BUTTONS)
                time.sleep(0.001)
    return path


def solve(grid: list[list[GridPixel]], start, end, algo):
    if algo:
        return a_star(grid, start, end)
    return bfs(grid, start, end)


def draw_path(grid, path):
    global PATH_FOUND
    PATH_FOUND = True
    for x, y in reversed(path):
        grid[x][y].color = RED
        draw(WIN, grid, BUTTONS)
        time.sleep(0.01)


def draw_grid(win: pygame.Surface, grid: list[list[GridPixel]]):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            if (i, j) == START or (i, j) == END:
                pygame.draw.rect(
                    win,
                    RED,
                    (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                )
                continue
            pygame.draw.rect(
                win,
                pixel.color,
                (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
            )
    # drawing grid lines
    for i in range(ROWS + 1):
        pygame.draw.line(win, BLACK, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))

    for i in range(COLS + 1):
        pygame.draw.line(
            win, BLACK, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT)
        )


def draw(win: pygame.Surface, grid: list[list[GridPixel]], buttons: list[Button]):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    pygame.display.update()


def get_pixel_from_mous_pos(mouse_pos):
    xcor, ycor = mouse_pos

    row = ycor // PIXEL_SIZE
    col = xcor // PIXEL_SIZE

    if row > ROWS or col >= COLS:
        raise IndexError

    return row, col


def init_grid() -> list[list[GridPixel]]:
    grid: list[list[GridPixel]] = []

    for i in range(ROWS):
        grid.append([])
        for _ in range(COLS):
            grid[i].append(GridPixel())
    return grid


def main():
    run = True
    clock = pygame.time.Clock()
    grid = init_grid()
    is_selecting_start = False
    is_selecting_end = False

    while run:
        clock.tick(MAX_FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()
                try:
                    global START
                    global END
                    row, col = get_pixel_from_mous_pos(mouse_pos)
                    if is_selecting_start:
                        grid[START[0]][START[1]].color = WHITE
                        START = (row, col)
                        is_selecting_start = False
                        grid[row][col].color = RED
                        continue
                    if is_selecting_end:
                        grid[END[0]][END[1]].color = WHITE
                        END = (row, col)
                        is_selecting_end = False
                        grid[row][col].color = RED
                        continue
                    grid[row][col].block_pixel()
                except IndexError:
                    for button in BUTTONS:
                        if not button.clicked(mouse_pos):
                            continue

                        global PATH_FOUND
                        if button.text == "SOLVE WITH A*":
                            if not PATH_FOUND:
                                path = solve(grid, START, END, True)
                                if len(path) == 0:
                                    print("No possible solution")
                                draw_path(grid, path)

                        if button.text == "SOLVE WITH BFS":
                            if not PATH_FOUND:
                                path = solve(grid, START, END, False)
                                if len(path) == 0:
                                    print("No possible solution")
                                    continue
                                draw_path(grid, path)

                        if button.text == "REDO":
                            PATH_FOUND = False
                            for i in range(ROWS):
                                for j in range(COLS):
                                    if not grid[i][j].is_blocked:
                                        grid[i][j].color = WHITE

                        if button.text == "CLEAR":
                            grid = init_grid()
                            PATH_FOUND = False

                        if button.text == "START":
                            print("Click pixel to select start")
                            is_selecting_end = False
                            is_selecting_start = True

                        if button.text == "END":
                            print("Click pixel to select end")
                            is_selecting_start = False
                            is_selecting_end = True

        draw(WIN, grid, BUTTONS)

    pygame.quit()


if __name__ == "__main__":
    main()
