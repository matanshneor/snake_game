"""
מחולל מבוכים — גרסת טרמינל
=============================
יוצר מבוך אקראי ומאפשר לנווט בו עם מקשי חצים או WASD.
אין צורך בדפדפן — רץ ישירות בטרמינל.

הרצה:
    python maze_terminal.py
"""

import random
import time
import os
import sys
import tty
import termios
from collections import deque

# ── צבעי ANSI לתצוגה בטרמינל ────────────────────────────────────────────────
WALL   = "\033[47m  \033[0m"    # קיר — אפור בהיר
PATH   = "\033[107m  \033[0m"   # נתיב — לבן בהיר
PLAYER = "\033[103m  \033[0m"   # שחקן — צהוב בהיר
START  = "\033[102m  \033[0m"   # נקודת התחלה — ירוק בהיר
END    = "\033[105m  \033[0m"   # נקודת סיום — סגול בהיר
TRAIL  = "\033[106m  \033[0m"   # שובל השחקן — תכלת בהיר


def create_grid(rows, cols):
    """יוצר רשת ריקה מלאה בקירות."""
    return [["#"] * cols for _ in range(rows)]


def generate_maze(rows, cols):
    """
    מייצר מבוך אקראי בשיטת Recursive Backtracking (DFS).

    האלגוריתם:
      - מתחיל מתא (1,1)
      - בוחר כיוון אקראי ומנפץ את הקיר לתא השכן (קפיצה של 2)
      - ממשיך רקורסיבית עד שכל התאים האפשריים בוקרו
    """
    grid = create_grid(rows, cols)

    def carve(r, c):
        """מנפץ נתיב מהתא הנוכחי לתאים שכנים לא-בוקרים."""
        grid[r][c] = " "
        directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "#":
                grid[r + dr // 2][c + dc // 2] = " "  # פתיחת הקיר בין שני התאים
                carve(nr, nc)

    carve(1, 1)
    return grid


def print_maze(grid, player=None, trail=None, start=None, end=None, message=""):
    """
    מדפיס את המבוך עם צבעי ANSI.

    פרמטרים:
        grid    — מטריצת המבוך
        player  — מיקום השחקן (שורה, עמודה)
        trail   — סט של תאים שהשחקן עבר בהם
        start   — נקודת ההתחלה
        end     — נקודת הסיום
        message — הודעה להדפסה מתחת למבוך
    """
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
    """
    קורא הקשת מקש בודדת מהמקלדת (כולל מקשי חצים).

    מקשי חצים נשלחים כרצף של 3 תווים: ESC + '[' + אות.
    הפונקציה מטפלת בזה ומחזירה את הרצף כמחרוזת אחת.
    """
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
        if ch == '\x1b':  # מקש חץ מתחיל ב-ESC
            ch2 = sys.stdin.read(1)
            ch3 = sys.stdin.read(1)
            return ch + ch2 + ch3
        return ch
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def play_maze(grid, start, end):
    """
    לולאת המשחק הראשית — ניווט אינטראקטיבי במבוך.

    שליטה:
        מקשי חצים או WASD — תנועה
        Q או Ctrl+C        — יציאה מהמשחק
    """
    player = start
    trail = set()          # תאים שהשחקן עבר בהם (לצביעת השובל)
    rows, cols = len(grid), len(grid[0])

    # קודי מקשי חצים
    ARROW_UP    = '\x1b[A'
    ARROW_DOWN  = '\x1b[B'
    ARROW_RIGHT = '\x1b[C'
    ARROW_LEFT  = '\x1b[D'

    # מיפוי מקשים לשינוי מיקום (שורה, עמודה)
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

        # יציאה מהמשחק
        if key in ('q', 'Q', '\x03'):
            print("\nGame quit.")
            break

        # תנועה — בדיקה שהתא החדש קיים ואינו קיר
        if key in moves:
            dr, dc = moves[key]
            nr, nc = player[0] + dr, player[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == " ":
                trail.add(player)      # מסמן את המיקום הקודם כשובל
                player = (nr, nc)

        print_maze(grid, player=player, trail=trail, start=start, end=end, message=hint)

        # בדיקת ניצחון — השחקן הגיע לנקודת הסיום
        if player == end:
            print(f"\n  You reached the exit in {len(trail) + 1} steps!  Congratulations!")
            break


def main():
    """נקודת הכניסה הראשית — מגדיר את גודל המבוך ומפעיל את המשחק."""
    sys.setrecursionlimit(100_000)  # נדרש כי generate_maze משתמשת ברקורסיה עמוקה

    ROWS, COLS = 21, 51  # חייבים להיות מספרים אי-זוגיים

    print("Generating maze...")
    time.sleep(0.3)

    grid = generate_maze(ROWS, COLS)

    start = (1, 1)
    end   = (ROWS - 2, COLS - 2)

    # פתיחת כניסה ויציאה בשוליים המבוך
    grid[0][1]           = " "
    grid[ROWS-1][COLS-2] = " "

    play_maze(grid, start, end)


if __name__ == "__main__":
    main()
