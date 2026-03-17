"""
Maze Generator with Player Navigation
Generates a random maze — navigate it using arrow keys or WASD
"""

import random
import time
import os
import sys
import tty
import termios
from collections import deque

# ANSI Colors — bright theme
WALL   = "\033[47m  \033[0m"    # Light gray wall
PATH   = "\033[107m  \033[0m"   # Bright white path
PLAYER = "\033[103m  \033[0m"   # Bright yellow player
START  = "\033[102m  \033[0m"   # Bright green start
END    = "\033[105m  \033[0m"   # Bright magenta end
TRAIL  = "\033[106m  \033[0m"   # Bright cyan trail


def create_grid(rows, cols):
    """Grid filled entirely with walls"""
    return [["#"] * cols for _ in range(rows)]


def generate_maze(rows, cols):
    """Generate maze using Recursive Backtracking (DFS)"""
    grid = create_grid(rows, cols)

    def carve(r, c):
        grid[r][c] = " "
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "#":
                grid[r + dr // 2][c + dc // 2] = " "  # break wall between cells
                carve(nr, nc)

    carve(1, 1)
    return grid


def print_maze(grid, player=None, trail=None, start=None, end=None, message=""):
    """Render the maze with colors"""
    trail = trail or set()
    os.system("clear")
    for r, row in enumerate(grid):
        line = ""
        for c, cell in enumerate(row):
            pos = (r, c)
            if pos == player:
                line += PLAYER
            elif pos == start:
                line += START
            elif pos == end:
                line += END
            elif pos in trail:
                line += TRAIL
            elif cell == "#":
                line += WALL
            else:
                line += PATH
        print(line)
    if message:
        print(f"\n{message}")


def get_key():
    """Read a single keypress (including arrow keys) from stdin"""
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def play_maze(grid, start, end):
    """Interactive maze navigation with arrow keys / WASD"""
    player = start
    trail = set()
    rows, cols = len(grid), len(grid[0])

    ARROW_UP    = '\x1b[A'
    ARROW_DOWN  = '\x1b[B'
    ARROW_RIGHT = '\x1b[C'
    ARROW_LEFT  = '\x1b[D'

    moves = {
        ARROW_UP:    (-1,  0),
        ARROW_DOWN:  ( 1,  0),
        ARROW_RIGHT: ( 0,  1),
        ARROW_LEFT:  ( 0, -1),
        'w': (-1,  0), 'W': (-1,  0),
        's': ( 1,  0), 'S': ( 1,  0),
        'd': ( 0,  1), 'D': ( 0,  1),
        'a': ( 0, -1), 'A': ( 0, -1),
    }

    hint = "Arrow keys or WASD to move  |  Q to quit"
    print_maze(grid, player=player, trail=trail, start=start, end=end, message=hint)

    while True:
        key = get_key()

        if key in ('q', 'Q', '\x03'):   # Q or Ctrl+C
            print("\nGame quit.")
            break

        if key in moves:
            dr, dc = moves[key]
            nr, nc = player[0] + dr, player[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == " ":
                trail.add(player)
                player = (nr, nc)

        print_maze(grid, player=player, trail=trail, start=start, end=end, message=hint)

        if player == end:
            print(f"\n  You reached the exit in {len(trail) + 1} steps!  Congratulations!")
            break


def main():
    sys.setrecursionlimit(100_000)

    ROWS, COLS = 21, 51  # must be odd numbers

    print("Generating maze...")
    time.sleep(0.3)

    grid = generate_maze(ROWS, COLS)

    start = (1, 1)
    end   = (ROWS - 2, COLS - 2)

    # Entry / exit openings
    grid[0][1]           = " "
    grid[ROWS-1][COLS-2] = " "

    play_maze(grid, start, end)


if __name__ == "__main__":
    main()
