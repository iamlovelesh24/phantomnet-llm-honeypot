"""
PhantomNet context store.

Provides session-scoped synthetic fact storage using SQLite.
Designed for defensive cyber-deception research only.
"""

import sqlite3
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


class ContextStore:
    """SQLite-backed context store with safe connection handling."""

    def __init__(self, db_path: Optional[str] = None):
        if db_path is None:
            db_path = "context.db"

        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self):
        """Create a short-lived SQLite connection."""
        return sqlite3.connect(str(self.db_path))

    def _initialize(self):
        """Create the context table."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS context_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    fact TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )
            conn.commit()

    def add_fact(self, session_id: str, fact: str) -> dict:
        """Store a synthetic fact for a session."""
        timestamp = datetime.utcnow().isoformat()

        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO context_facts
                (session_id, fact, created_at)
                VALUES (?, ?, ?)
                """,
                (session_id, fact, timestamp),
            )
            conn.commit()

            return {
                "success": True,
                "id": cursor.lastrowid,
                "session_id": session_id,
                "fact": fact,
                "created_at": timestamp,
            }

    def retrieve(
        self,
        session_id: str,
        query: str,
        max_age_minutes: int = 10,
    ) -> list:
        """Retrieve recent facts for a session matching the query."""
        cutoff = datetime.utcnow() - timedelta(minutes=max_age_minutes)

        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, session_id, fact, created_at
                FROM context_facts
                WHERE session_id = ?
                  AND created_at >= ?
                  AND LOWER(fact) LIKE ?
                ORDER BY id DESC
                """,
                (
                    session_id,
                    cutoff.isoformat(),
                    "%" + query.lower() + "%",
                ),
            ).fetchall()

        return [
            {
                "id": row[0],
                "session_id": row[1],
                "fact": row[2],
                "created_at": row[3],
            }
            for row in rows
        ]

    def get_session_facts(self, session_id: str) -> list:
        """Return all facts for a session."""
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, session_id, fact, created_at
                FROM context_facts
                WHERE session_id = ?
                ORDER BY id
                """,
                (session_id,),
            ).fetchall()

        return [
            {
                "id": row[0],
                "session_id": row[1],
                "fact": row[2],
                "created_at": row[3],
            }
            for row in rows
        ]

    def status(self) -> dict:
        """Return context store health information."""
        with self._connect() as conn:
            count = conn.execute(
                "SELECT COUNT(*) FROM context_facts"
            ).fetchone()[0]

        return {
            "status": "ok",
            "backend": "sqlite",
            "database": str(self.db_path),
            "fact_count": count,
        }

    def close(self):
        """Compatibility method; connections are short-lived."""
        return None