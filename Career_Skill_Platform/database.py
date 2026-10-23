import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "career_skill_platform.db"

def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection

def init_db():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                education TEXT DEFAULT '',
                career TEXT DEFAULT '',
                known_skills TEXT DEFAULT '',
                skill_levels TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                skill TEXT NOT NULL,
                topic TEXT NOT NULL,
                completed INTEGER DEFAULT 0,
                UNIQUE(email, skill, topic)
            )
        """)

def save_student(name, email, education, career, known_skills, skill_levels):
    with get_connection() as conn:
        existing = conn.execute("SELECT id FROM students WHERE email = ?", (email,)).fetchone()
        if existing:
            conn.execute("""
                UPDATE students
                SET name=?, education=?, career=?, known_skills=?, skill_levels=?
                WHERE email=?
            """, (name, education, career, known_skills, skill_levels, email))
        else:
            conn.execute("""
                INSERT INTO students (name, email, education, career, known_skills, skill_levels)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, email, education, career, known_skills, skill_levels))

def get_student(email):
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        return dict(row) if row else None

def save_learning_progress(email, skill, topic, completed):
    with get_connection() as conn:
        conn.execute("""
            INSERT INTO learning_progress (email, skill, topic, completed)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(email, skill, topic) DO UPDATE SET completed=excluded.completed
        """, (email, skill, topic, int(bool(completed))))

def get_learning_progress(email):
    with get_connection() as conn:
        rows = conn.execute("""
            SELECT skill, topic, completed FROM learning_progress
            WHERE email = ? ORDER BY skill, topic
        """, (email,)).fetchall()
        return [dict(row) for row in rows]
