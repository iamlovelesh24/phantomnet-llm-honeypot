"""
PhantomNet LLM safety guardrails.

Ensures generated content remains synthetic and inside
the controlled PhantomNet deception environment.
"""

FORBIDDEN_REAL_DATA_TERMS = [
    "real employee",
    "real customer",
    "production credential",
    "actual password",
    "real password",
    "social security number",
    "credit card number",
]

SAFETY_RULES = [
    "Only generate synthetic fictional information.",
    "Never expose real credentials or secrets.",
    "Never use real employee or customer information.",
    "Never provide instructions for attacking real systems.",
    "Keep generated content inside the PhantomNet environment.",
]


def validate_input(text: str) -> bool:
    """
    Check whether an input contains prohibited real-world data requests.
    """
    normalized = text.lower()

    for term in FORBIDDEN_REAL_DATA_TERMS:
        if term in normalized:
            return False

    return True


def validate_output(text: str) -> bool:
    """
    Basic validation for generated PhantomNet content.
    """
    if not text or not text.strip():
        return False

    return True


def safety_message() -> str:
    """
    Return the standard PhantomNet safety message.
    """
    return (
        "PhantomNet generates synthetic data only "
        "inside a controlled deception environment."
    )
