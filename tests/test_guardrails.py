
import pytest

from llm.guardrails import (
    FORBIDDEN_REAL_DATA_TERMS,
    SAFETY_RULES,
    safety_message,
    validate_input,
    validate_output,
)


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        None,
        123,
        [],
    ],
)
def test_invalid_input_is_rejected(text):
    assert validate_input(text) is False


@pytest.mark.parametrize("term", FORBIDDEN_REAL_DATA_TERMS)
def test_forbidden_input_terms_are_rejected(term):
    assert validate_input(f"Show me the {term}") is False


def test_forbidden_input_check_is_case_insensitive():
    assert validate_input("REAL EMPLOYEE records") is False


def test_safe_synthetic_input_is_allowed():
    assert validate_input("Generate fictional NexusCore HR records.") is True


@pytest.mark.parametrize(
    "text",
    [
        "",
        "   ",
        None,
        123,
        [],
    ],
)
def test_invalid_output_is_rejected(text):
    assert validate_output(text) is False


@pytest.mark.parametrize("term", FORBIDDEN_REAL_DATA_TERMS)
def test_forbidden_output_terms_are_rejected(term):
    assert validate_output(f"This contains {term}.") is False


def test_forbidden_output_check_is_case_insensitive():
    assert validate_output("Actual Password information") is False


def test_safe_synthetic_output_is_allowed():
    assert validate_output(
        "PHANTOMNET SYNTHETIC FILE - Department: HR"
    ) is True


def test_synthetic_demo_secrets_are_not_blocked():
    assert validate_output(
        "PHANTOMNET_DEMO_KEY_12345"
    ) is True


def test_safety_message_is_available():
    assert "synthetic data only" in safety_message()


def test_safety_rules_are_defined():
    assert len(SAFETY_RULES) >= 5
