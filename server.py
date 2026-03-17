"""
Snake Game - Backend Server
Saves high scores and serves the game.
Run:  python server.py
Then open: http://localhost:5000
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os
from datetime import datetime

app = Flask(__name__)
CORS(app)

SCORES_FILE = 'scores.json'


def load_scores():
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f:
            return json.load(f)
    return []


def save_scores(scores):
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)


# ── Serve the game ──────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'snake.html')


# ── Scores API ──────────────────────────────────────────
@app.route('/scores', methods=['GET'])
def get_scores():
    scores = load_scores()
    level = request.args.get('level')
    if level:
        scores = [s for s in scores if s.get('level') == level]
    scores.sort(key=lambda x: (float(x['time']), int(x['steps'])))
    return jsonify(scores[:10])


@app.route('/scores', methods=['POST'])
def add_score():
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'error': 'missing data'}), 400
    scores = load_scores()
    scores.append({
        'username': data['username'].strip()[:20] or 'Anonymous',
        'time':     round(float(data['time']), 2),
        'steps':    int(data['steps']),
        'level':    data.get('level', 'Medium'),
        'date':     datetime.now().strftime('%Y-%m-%d'),
    })
    save_scores(scores)
    return jsonify({'ok': True})


if __name__ == '__main__':
    # Auto-install dependencies if missing
    try:
        import flask_cors
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask', 'flask-cors'])

    print("\n🐍 Snake Game Server running at http://localhost:8080\n")
    app.run(debug=True, port=8080)
