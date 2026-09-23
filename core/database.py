import sqlite3
import json
from pathlib import Path


# Database location
DB_PATH = Path(__file__).resolve().parent.parent / "secmate.db"


def get_connection():
    """Create a database connection."""
    return sqlite3.connect(DB_PATH)


def initialize_database():
    """Create the assessments table if it does not exist."""

    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS assessments (
                assessment_id TEXT PRIMARY KEY,
                target TEXT NOT NULL,
                verdict TEXT,
                severity TEXT,
                timestamp TEXT,
                report_json TEXT NOT NULL
            )
        """)

        conn.commit()


def save_assessment(assessment):
    """Save an assessment report to SQLite."""

    with get_connection() as conn:
        conn.execute("""
            INSERT OR REPLACE INTO assessments (
                assessment_id,
                target,
                verdict,
                severity,
                timestamp,
                report_json
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            assessment["assessment_id"],
            assessment["target"],
            assessment["verdict"],
            assessment["severity"],
            assessment["timestamp"],
            json.dumps(assessment)
        ))

        conn.commit()


def get_all_assessments():
    """Retrieve all saved assessments."""

    with get_connection() as conn:
        rows = conn.execute("""
            SELECT report_json
            FROM assessments
            ORDER BY timestamp DESC
        """).fetchall()

    return [json.loads(row[0]) for row in rows]