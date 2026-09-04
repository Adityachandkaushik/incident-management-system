import sqlite3
from pathlib import Path

from flask import current_app


def get_db():
    db_path = Path(current_app.config["DATABASE_PATH"])

    db_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    conn = sqlite3.connect(str(db_path))

    conn.row_factory = sqlite3.Row

    return conn

def init_db():
    conn = get_db()

    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user'
        );

        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            priority TEXT NOT NULL DEFAULT 'Medium',
            status TEXT NOT NULL DEFAULT 'Open',
            created_by INTEGER,
            assigned_to INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,

            FOREIGN KEY (created_by)
                REFERENCES users(id),

            FOREIGN KEY (assigned_to)
                REFERENCES users(id)
        );
    """)

    conn.commit()
    conn.close()