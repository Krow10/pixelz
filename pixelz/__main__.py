"""
Main entry point
"""
import curses
from random import randint, random

def put_pixel(stdscr: 'curses._CursesWindow', x: int, y: int, color: int) -> None:
    try:
        stdscr.addch(y, x, '■', color)
    except Exception as e:
        raise TypeError(
            f'Could not place pixel at ({y}, {x}): max is {stdscr.getmaxyx()}'
        ) from e

def safe_index(l: list[list] | list, i: int, j: int | None = None) -> int:
    if i < 0:
        return 0

    try:
        if j is not None:
            if j < 0:
                return 0

            return l[i][j]
        else:
            return l[i]
    except IndexError:
        return 0

def main(stdscr: 'curses._CursesWindow', num_players: int = 2) -> None:
    # Init colors
    curses.start_color()
    curses.use_default_colors()
    for i in range(0, curses.COLORS):
        curses.init_pair(i + 1, i, -1)

    stdscr.nodelay(1) # Non-blocking I/O, set to 0 for step-by-step or 1 for real-time

    # TODO: Select opposite / nice contrast colors for players
    fighters = [randint(0, curses.COLORS) for _ in range(num_players)]
    max_height, max_width = stdscr.getmaxyx()
    running = True
    show_info = False

    # Assuming only 2 players for now
    board_matrix = [
        (
            [0 for _ in range(max_width // 2)] +
            [1 for _ in range(max_width // 2)]
        ) for _ in range(max_height)
    ] # TODO: Fix sizing issues for odd terminal sizes

    max_width, max_height = (len(board_matrix[0]), len(board_matrix)) # Resize according to maximum screen size filled

    # Calculate maximum neighbours for each position (8 default, 5 on the sides and 3 in the corners)
    neighbours_matrix = [[8 for _ in range(max_width)] for _ in range(max_height)]

    for x in range(max_width):
        neighbours_matrix[0][x] = 5
        neighbours_matrix[max_height - 1][x] = 5

    for y in range(max_height):
        neighbours_matrix[y][0] = 5
        neighbours_matrix[y][max_width - 1] = 5

    neighbours_matrix[0][0] = \
    neighbours_matrix[0][max_width - 1] = \
    neighbours_matrix[max_height - 1][max_width - 1] = \
    neighbours_matrix[max_height - 1][0] = 3

    while running:
        # Draw current board state
        for y, row in enumerate(board_matrix):
            for x, player in enumerate(row):
                put_pixel(stdscr, x, y, curses.color_pair(fighters[player]))

        # Show statistics
        if show_info:
            win_ratio = sum(sum(row) for row in board_matrix)/(max_height*max_width)
            stdscr.addstr(
                0,
                max_width//2 + 1 - len(str(round(win_ratio, 4))),
                f'{round(win_ratio, 4)}',
                curses.color_pair(fighters[win_ratio > .5])
            )

        # Update board
        flip = []
        for y, row in enumerate(board_matrix):
            for x, player in enumerate(row):
                # Compute ratio of same color cells to maximum neighbours
                ratio = (
                    safe_index(board_matrix, y-1, x) +
                    safe_index(board_matrix, y-1, x-1) +
                    safe_index(board_matrix, y-1, x+1) +
                    safe_index(board_matrix, y+1, x) +
                    safe_index(board_matrix, y+1, x-1) +
                    safe_index(board_matrix, y+1, x+1) +
                    safe_index(row, x-1) +
                    safe_index(row, x+1)
                ) / neighbours_matrix[y][x]

                # If ratio is not high enough (e.g. surrounded by some opposite color pixelz), colors will be flipped
                threshold = random()
                if int(ratio > threshold) != player:
                    flip.append((y, x))

        # Flip colors for fallen pixelz
        for (y, x) in flip:
            board_matrix[y][x] = 1 - board_matrix[y][x]

        stdscr.refresh()

        user_input = stdscr.getch()
        if user_input > 0:
            user_input = chr(user_input).lower()

            # TODO: Add space for pause / resume
            if user_input == 'i':
                show_info = not show_info
            running = user_input != 'q'

curses.wrapper(main)
