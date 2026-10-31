"""
Persistent telemetry service for PhantomNet Member 3.

Stores normalized events in SQLite and provides
a clean interface for Member 4 dashboard integration.
"""

from __future__ import annotations

import json
import sqlite3
import uuid

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional


DATABASE_PATH = Path("phantomnet.db")


def _timestamp() -> str:

    return datetime.now(
        timezone.utc
    ).isoformat()


def initialize_telemetry_db() -> None:

    connection = sqlite3.connect(
        DATABASE_PATH
    )

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


def record_event(
    session_id: str,
    event_type: str,
    action: str,
    response: Optional[Any] = None,
    module: str = "member3",
    behavior: Optional[Dict[str, Any]] = None,
    scenario: Optional[str] = None,
    risk_level: Optional[str] = None,
    risk_score: Optional[float] = None,
) -> Dict[str, Any]:

    initialize_telemetry_db()

    event_id = str(uuid.uuid4())
    timestamp = _timestamp()

    metadata = {
        "response": response,
        "module": module,
        "behavior": behavior or {},
    }

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.execute(
        """
        INSERT INTO telemetry_events
        (
            event_id,
            session_id,
            timestamp,
            event_type,
            action,
            scenario,
            risk_level,
            risk_score,
            metadata
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            event_id,
            session_id,
            timestamp,
            event_type,
            action,
            scenario,
            risk_level,
            risk_score,
            json.dumps(metadata),
        ),
    )

    connection.commit()
    connection.close()

    return {
        "event_id": event_id,
        "session_id": session_id,
        "timestamp": timestamp,
        "event_type": event_type,
        "action": action,
        "scenario": scenario,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "metadata": metadata,
    }


def get_events(
    session_id: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:

    initialize_telemetry_db()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    if session_id:

        rows = connection.execute(
            """
            SELECT *
            FROM telemetry_events
            WHERE session_id = ?
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (
                session_id,
                limit,
            ),
        ).fetchall()

    else:

        rows = connection.execute(
            """
            SELECT *
            FROM telemetry_events
            ORDER BY timestamp DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    connection.close()

    result = []

    for row in rows:

        item = dict(row)

        try:
            item["metadata"] = json.loads(
                item.get("metadata") or "{}"
            )
        except json.JSONDecodeError:
            pass

        result.append(item)

    return result


def health() -> Dict[str, Any]:

    initialize_telemetry_db()

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    count = connection.execute(
        "SELECT COUNT(*) FROM telemetry_events"
    ).fetchone()[0]

    connection.close()

    return {
        "service": "member3-telemetry",
        "database": str(DATABASE_PATH),
        "event_count": count,
        "status": "ready",
    }
