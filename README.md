# Snake Game — Kids Maze Game

A fun and colorful maze game for kids! Navigate through randomly generated mazes using keyboard controls. Supports 1-player and 2-player modes.

## How to Play

### Without a server (no leaderboard)
Open `snake.html` directly in your browser — no installation needed.

### With the leaderboard server
```bash
python server.py
```
Then open [http://localhost:8080](http://localhost:8080)

## Game Modes

### 1 Player
- Use **arrow keys** to navigate from the blue square to the house exit
- Finish as fast as possible — your time and steps are recorded
- Top scores appear on the side leaderboard

### 2 Players (same keyboard)
| Player | Controls |
|--------|----------|
| 🟠 Player 1 | Arrow keys |
| 🔵 Player 2 | WASD |

Race to the exit — first to arrive wins!

## Features

- **Random maze generation** — every game is unique
- **4 difficulty levels** — Easy, Medium, Hard, Extreme
- **Auto Solve** — BFS shortest-path animation
- **1P leaderboard** — saved scores per difficulty level (requires `server.py`)
- **2P wins scoreboard** — tracks wins per session
- **Switch modes** — toggle between 1P and 2P mid-session
- **Background music** — looping melody with toggle button
- **Victory screen** — confetti, balloons & applause

## Files

| File | Description |
|------|-------------|
| `snake.html` | Main game — open in any modern browser |
| `server.py` | Flask backend — saves scores to `scores.json` |
| `maze_terminal.py` | Terminal version of the maze (Python, no browser needed) |

## Running the Terminal Version

```bash
python maze_terminal.py
```
Navigate with arrow keys or WASD. Press **Q** to quit.

## Tech Stack

- **HTML5 Canvas** — maze rendering
- **Web Audio API** — background music & sound effects
- **Vanilla JavaScript** — no libraries or frameworks
- **Python / Flask** — optional backend for the leaderboard
