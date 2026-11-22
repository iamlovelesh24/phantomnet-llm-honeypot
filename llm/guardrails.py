
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


def _contains_forbidden_term(text: str) -> bool:
    """Check text for prohibited real-world data references."""
    normalized = text.casefold()

    return any(
        term.casefold() in normalized
        for term in FORBIDDEN_REAL_DATA_TERMS
    )


def validate_input(text: str) -> bool:
    """Reject invalid or prohibited user prompts."""
    if not isinstance(text, str) or not text.strip():
        return False

    return not _contains_forbidden_term(text)


def validate_output(text: str) -> bool:
    """Reject empty, invalid, or prohibited generated content."""
    if not isinstance(text, str) or not text.strip():
        return False

    return not _contains_forbidden_term(text)


def safety_message() -> str:
    """Return the standard PhantomNet safety message."""
    return (
        "PhantomNet generates synthetic data only "
        "inside a controlled deception environment."
    )
