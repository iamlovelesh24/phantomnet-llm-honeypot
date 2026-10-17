"""
PhantomNet database layer.

Provides a lightweight SQLite database for storing
telemetry events and session information.
"""

import sqlite3
from pathlib import Path


DATABASE_PATH = Path("phantomnet.db")


def get_connection():
    """Create and return a SQLite database connection."""
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    """Create the telemetry table if it does not already exist."""
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS telemetry_events (
            event_id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            event_type TEXT NOT NULL,
            action TEXT NOT NULL,
            scenario TEXT,
            risk_level TEXT,
            risk_score REAL,
            metadata TEXT
        )
        """
    )

    connection.commit()
    connection.close()
