"""
PhantomNet deception scenarios.

Defines safe simulated attacker activities that can be
recorded and analyzed by the telemetry system.
"""

DECEPTION_SCENARIOS = {
    "network_discovery": {
        "description": "Simulated internal network discovery activity.",
        "risk_level": "low",
        "indicators": [
            "port_scan",
            "host_discovery",
            "service_enumeration",
        ],
    },

    "file_discovery": {
        "description": "Simulated exploration of files and directories.",
        "risk_level": "low",
        "indicators": [
            "directory_listing",
            "file_search",
            "configuration_file_access",
        ],
    },

    "credential_probing": {
        "description": "Simulated search for credential-related information.",
        "risk_level": "high",
        "indicators": [
            "credential_file_search",
            "password_file_access",
            "secret_key_search",
        ],
    },

    "sensitive_database_query": {
        "description": "Simulated query for sensitive corporate information.",
        "risk_level": "high",
        "indicators": [
            "payroll_query",
            "employee_data_query",
            "financial_data_query",
        ],
    },

    "cloud_secret_search": {
        "description": "Simulated search for cloud credentials or keys.",
        "risk_level": "critical",
        "indicators": [
            "aws_key_search",
            "cloud_token_search",
            "api_key_search",
        ],
    },

    "repeated_suspicious_activity": {
        "description": "Repeated simulated activity targeting sensitive resources.",
        "risk_level": "critical",
        "indicators": [
            "repeated_sensitive_access",
            "credential_probing",
            "secret_search",
        ],
    },
}


def get_scenario(scenario_name: str):
    """Return a deception scenario by name."""
    return DECEPTION_SCENARIOS.get(scenario_name)


def list_scenarios():
    """Return all available deception scenario names."""
    return list(DECEPTION_SCENARIOS.keys())
