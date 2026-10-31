"""
PhantomNet deception scenarios.

Member 2:
Generative FUSE Filesystem & Deception Shell

All values returned by this module are synthetic and exist only
for the PhantomNet deception environment.
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


def get_scenario(filename: str) -> str | None:
    """Return synthetic deception content for a known scenario."""
    if filename == SECRET_KEYS_SCENARIO["filename"]:
        return SECRET_KEYS_SCENARIO["content"]

    return None
