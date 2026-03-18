"""
שרת Backend למשחק Snake
========================
מספק שני שירותים:
  1. הגשת קובץ המשחק (snake.html) בגישה לכתובת http://localhost:8080
  2. שמירת ניקודים וקריאת לוח שיאים דרך API

הרצה:
    python server.py

תלויות:
    pip install flask flask-cors
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import json, os
from datetime import datetime

app = Flask(__name__)
CORS(app)  # מאפשר גישה מהדפדפן גם כשהדפדפן נמצא בדומיין שונה

SCORES_FILE = 'scores.json'  # קובץ שמירת הניקודים


def load_scores():
    """קורא את כל הניקודים מהקובץ. מחזיר רשימה ריקה אם הקובץ לא קיים."""
    if os.path.exists(SCORES_FILE):
        with open(SCORES_FILE) as f:
            return json.load(f)
    return []


def save_scores(scores):
    """שומר את רשימת הניקודים לקובץ JSON."""
    with open(SCORES_FILE, 'w') as f:
        json.dump(scores, f, indent=2, ensure_ascii=False)


# ── הגשת המשחק ──────────────────────────────────────────────────────────────

@app.route('/')
def index():
    """מגיש את קובץ המשחק snake.html כשנכנסים לכתובת הראשית."""
    return send_from_directory('.', 'snake.html')


# ── API ניקודים ──────────────────────────────────────────────────────────────

@app.route('/scores', methods=['GET'])
def get_scores():
    """
    מחזיר את עשרת הניקודים הגבוהים ביותר.

    פרמטר אופציונלי:
        ?level=Easy|Medium|Hard|Extreme  — סינון לפי רמת קושי

    מיון: לפי זמן (מהיר ביותר קודם), במקרה שוויון — לפי מספר צעדים.
    """
    scores = load_scores()
    level = request.args.get('level')
    if level:
        scores = [s for s in scores if s.get('level') == level]
    scores.sort(key=lambda x: (float(x['time']), int(x['steps'])))
    return jsonify(scores[:10])


@app.route('/scores', methods=['POST'])
def add_score():
    """
    מקבל ניקוד חדש ושומר אותו בקובץ.

    גוף הבקשה (JSON):
        username  — שם השחקן (חובה)
        time      — זמן בשניות
        steps     — מספר צעדים
        level     — רמת קושי (אופציונלי, ברירת מחדל: Medium)
    """
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


# ── הפעלה ───────────────────────────────────────────────────────────────────

if __name__ == '__main__':
    # התקנה אוטומטית של תלויות חסרות
    try:
        import flask_cors
    except ImportError:
        import subprocess, sys
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'flask', 'flask-cors'])

    print("\n🐍 Snake Game Server running at http://localhost:8080\n")
    app.run(debug=True, port=8080)
