"""
PhantomNet context store.

Provides short-lived session context persistence using SQLite.
All data is synthetic and intended for isolated defensive research.
"""

import sqlite3
import time
from pathlib import Path


class ContextStore:
    def __init__(self, db_path=None, ttl_seconds=600):
        self.db_path = Path(db_path or "context.db")
        self.ttl_seconds = ttl_seconds
        self._initialize()

    def _connect(self):
        connection = sqlite3.connect(
            str(self.db_path),
            timeout=5,
        )
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize(self):
        connection = self._connect()
        try:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS context_facts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    fact TEXT NOT NULL,
                    created_at REAL NOT NULL
                )
                """
            )
            connection.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_context_session
                ON context_facts(session_id)
                """
            )
            connection.commit()
        finally:
            connection.close()

    def add_fact(self, session_id, fact):
        connection = self._connect()
        try:
            now = time.time()

            connection.execute(
                """
                DELETE FROM context_facts
                WHERE created_at < ?
                """,
                (now - self.ttl_seconds,),
            )

            connection.execute(
                """
                INSERT INTO context_facts(session_id, fact, created_at)
                VALUES (?, ?, ?)
                """,
                (session_id, fact, now),
            )

            connection.commit()

            return {
                "success": True,
                "session_id": session_id,
                "fact": fact,
            }
        finally:
            connection.close()

    def retrieve(self, session_id, query=None):
        connection = self._connect()
        try:
            now = time.time()

            connection.execute(
                """
                DELETE FROM context_facts
                WHERE created_at < ?
                """,
                (now - self.ttl_seconds,),
            )
            connection.commit()

            rows = connection.execute(
                """
                SELECT fact
                FROM context_facts
                WHERE session_id = ?
                ORDER BY id ASC
                """,
                (session_id,),
            ).fetchall()

            facts = [row["fact"] for row in rows]

            if query:
                query_lower = query.lower()
                matching = [
                    fact
                    for fact in facts
                    if query_lower in fact.lower()
                ]

                if matching:
                    facts = matching

            return facts
        finally:
            connection.close()

    def status(self):
        connection = self._connect()
        try:
            count = connection.execute(
                "SELECT COUNT(*) AS count FROM context_facts"
            ).fetchone()["count"]

            return {
                "backend": "sqlite",
                "database": str(self.db_path),
                "ttl_seconds": self.ttl_seconds,
                "fact_count": count,
                "healthy": True,
            }
        finally:
            connection.close()

    def close(self):
        """
        Compatibility method.

        Connections are intentionally short-lived, so there is
        no persistent connection to close.
        """
        return None