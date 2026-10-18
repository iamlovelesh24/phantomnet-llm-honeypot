"""
PhantomNet database models.

Defines the structure used for telemetry event persistence.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TelemetryRecord:
    event_id: str
    session_id: str
    timestamp: str
    event_type: str
    action: str
    scenario: Optional[str] = None
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    metadata: Optional[str] = None
