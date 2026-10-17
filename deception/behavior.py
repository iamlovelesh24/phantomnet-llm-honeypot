"""
PhantomNet behavior analysis.

Classifies simulated attacker activities into risk levels
for telemetry and security dashboard analysis.
"""


BEHAVIOR_RULES = {
    "port_scan": {
        "category": "network_discovery",
        "risk_level": "low",
        "score": 20,
    },
    "host_discovery": {
        "category": "network_discovery",
        "risk_level": "low",
        "score": 25,
    },
    "file_discovery": {
        "category": "file_discovery",
        "risk_level": "low",
        "score": 20,
    },
    "service_enumeration": {
        "category": "network_discovery",
        "risk_level": "medium",
        "score": 40,
    },
    "credential_probing": {
        "category": "credential_access",
        "risk_level": "medium",
        "score": 55,
    },
    "secret_key_discovery": {
        "category": "credential_access",
        "risk_level": "high",
        "score": 75,
    },
    "ransomware_activity": {
        "category": "impact",
        "risk_level": "critical",
        "score": 95,
    },
}


def analyze_behavior(activity: str) -> dict:
    """
    Analyze a simulated attacker activity.

    Returns a structured risk assessment.
    """

    activity_key = activity.lower().strip()

    result = BEHAVIOR_RULES.get(
        activity_key,
        {
            "category": "unknown",
            "risk_level": "unknown",
            "score": 0,
        },
    )

    return {
        "activity": activity_key,
        **result,
    }


def list_behaviors() -> list:
    """Return all supported simulated behaviors."""

    return list(BEHAVIOR_RULES.keys())
