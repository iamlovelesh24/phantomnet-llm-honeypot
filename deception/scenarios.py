"""
PhantomNet synthetic deception scenarios.

Combines Member 2's synthetic filesystem content with Member 3's
telemetry scenario definitions. No real credentials are used.
"""

SECRET_KEYS_SCENARIO = {
    "filename": "secret_keys.txt",
    "title": "Synthetic API Key Store",
    "content": """PHANTOMNET SYNTHETIC SECRET STORE
================================

WARNING: This is simulated deception data.

Service: internal-api
Environment: phantomnet-demo

API_KEY=PHANTOMNET_DEMO_KEY_7F3A9C21
API_SECRET=PHANTOMNET_DEMO_SECRET_4B82E611
TOKEN=PHANTOMNET_SIMULATED_TOKEN_91A7D4

These values are synthetic and must never be used
for authentication or access to real systems.
""",
}

DECEPTION_SCENARIOS = {
    "network_discovery": {
        "description": "Simulated internal network discovery activity.",
        "risk_level": "low",
        "indicators": ["port_scan", "host_discovery", "service_enumeration"],
    },
    "file_discovery": {
        "description": "Simulated exploration of files and directories.",
        "risk_level": "low",
        "indicators": ["directory_listing", "file_search", "configuration_file_access"],
    },
    "credential_probing": {
        "description": "Simulated search for credential-related information.",
        "risk_level": "high",
        "indicators": ["credential_file_search", "password_file_access", "secret_key_search"],
    },
    "sensitive_database_query": {
        "description": "Simulated query for sensitive corporate information.",
        "risk_level": "high",
        "indicators": ["payroll_query", "employee_data_query", "financial_data_query"],
    },
    "cloud_secret_search": {
        "description": "Simulated search for cloud credentials or keys.",
        "risk_level": "critical",
        "indicators": ["aws_key_search", "cloud_token_search", "api_key_search"],
    },
    "repeated_suspicious_activity": {
        "description": "Repeated simulated activity targeting sensitive resources.",
        "risk_level": "critical",
        "indicators": ["repeated_sensitive_access", "credential_probing", "secret_search"],
    },
}


def get_scenario(name: str):
    """Return synthetic file contents by filename or a telemetry scenario by name."""
    if name == SECRET_KEYS_SCENARIO["filename"]:
        return SECRET_KEYS_SCENARIO["content"]
    return DECEPTION_SCENARIOS.get(name)


def list_scenarios():
    """Return all available telemetry scenario names."""
    return list(DECEPTION_SCENARIOS.keys())
