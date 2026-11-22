import pytest
from unittest.mock import patch

from deception.file_generator import (
    FileGenerator,
    validate_generated_content,
)


# -------------------------------
# Content validation tests
# -------------------------------

def test_valid_synthetic_content_is_accepted():
    content = "PHANTOMNET SYNTHETIC FILE - Internal Simulation"

    assert validate_generated_content(content) is True


def test_empty_content_is_rejected():
    assert validate_generated_content("") is False


def test_whitespace_content_is_rejected():
    assert validate_generated_content("   ") is False


def test_non_string_content_is_rejected():
    assert validate_generated_content(None) is False


def test_unknown_employee_id_is_rejected():
    content = "Employee reference: NC-EMP-9999"

    assert validate_generated_content(content) is False


def test_unknown_project_id_is_rejected():
    content = "Project reference: NC-PRJ-9999"

    assert validate_generated_content(content) is False


def test_forbidden_real_data_term_is_rejected():
    from llm.guardrails import FORBIDDEN_REAL_DATA_TERMS

    if not FORBIDDEN_REAL_DATA_TERMS:
        pytest.skip("No forbidden terms configured")

    content = f"Reference: {FORBIDDEN_REAL_DATA_TERMS[0]}"

    assert validate_generated_content(content) is False


# -------------------------------
# LLM fallback test
# -------------------------------

def test_invalid_llm_content_triggers_fallback(monkeypatch):
    monkeypatch.setenv("PHANTOMNET_ENABLE_LLM_CONTENT", "true")

    generator = FileGenerator("session-test")

    with patch(
        "deception.file_generator.llm_generate",
        return_value="Employee reference: NC-EMP-9999",
    ):
        generated = generator.generate("/HR/employees.txt")

    assert "PHANTOMNET SYNTHETIC FILE" in generated.content
    assert "NC-EMP-9999" not in generated.content
    assert "Synthetic Demo Data" in generated.content