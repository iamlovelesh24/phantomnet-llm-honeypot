"""
PhantomNet telemetry collection.

Records simulated attacker activity for monitoring and analysis.
This module stores structured events in memory so they can later
be connected to the PhantomNet database layer.
"""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4


def create_event(
    event_type: str,
    action: str,
    scenario: Optional[str] = None,
    risk_level: Optional[str] = None,
    risk_score: Optional[int] = None,
    metadata: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a structured telemetry event.

    Parameters:
        event_type: Type of activity being recorded.
        action: Simulated action or command.
        scenario: Related deception scenario.
        risk_level: Risk classification such as low, medium, or high.
        risk_score: Numeric risk score.
        metadata: Additional event information.
        session_id: Existing session identifier, if available.

    Returns:
        A structured telemetry event dictionary.
    """

    return {
        "event_id": str(uuid4()),
        "session_id": session_id or str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type,
        "action": action,
        "scenario": scenario,
        "risk_level": risk_level,
        "risk_score": risk_score,
        "metadata": metadata or {},
    }


def record_event(
    events: List[Dict[str, Any]],
    event: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Add a telemetry event to the current session event list.

    Returns:
        The recorded event.
    """

    events.append(event)
    return event


def get_session_events(
    events: List[Dict[str, Any]],
    session_id: str,
) -> List[Dict[str, Any]]:
    """
    Return all telemetry events belonging to a session.
    """

    return [
        event
        for event in events
        if event.get("session_id") == session_id
    ]


def summarize_session(
    events: List[Dict[str, Any]],
    session_id: str,
) -> Dict[str, Any]:
    """
    Create a basic summary of activity for a simulated session.
    """

    session_events = get_session_events(events, session_id)

    risk_scores = [
        event["risk_score"]
        for event in session_events
        if isinstance(event.get("risk_score"), (int, float))
    ]

    return {
        "session_id": session_id,
        "event_count": len(session_events),
        "max_risk_score": max(risk_scores) if risk_scores else 0,
        "event_types": sorted(
            {
                event.get("event_type")
                for event in session_events
                if event.get("event_type")
            }
        ),
    }
