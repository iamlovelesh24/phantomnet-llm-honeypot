import pytest

from evaluation.prompt_consistency import (
    validate_output,
    evaluate_project_consistency,
    ALLOWED_EMPLOYEE_IDS,
    PROJECT_IDS,
)


def test_valid_atlas_output():
    output = "Project Atlas (NC-PRJ-0001) is progressing well."
    passed, result = validate_output(output, "Atlas")

    assert passed is True
    assert result == output


def test_empty_output_rejected():
    passed, _ = validate_output("", "Atlas")
    assert passed is False


def test_invalid_project_rejected():
    passed, _ = validate_output("Project Unknown update", "Unknown")
    assert passed is False


def test_missing_project_name_rejected():
    passed, _ = validate_output("General company update.", "Atlas")
    assert passed is False


@pytest.mark.parametrize(
    "term",
    ["Alice Johnson", "Bob Smith", "P101", "Acme Corp"],
)
def test_forbidden_terms_rejected(term):
    output = f"Project Atlas update mentions {term}."
    passed, _ = validate_output(output, "Atlas")

    assert passed is False


@pytest.mark.parametrize(
    "employee_id",
    sorted(ALLOWED_EMPLOYEE_IDS),
)
def test_approved_employee_ids_accepted(employee_id):
    output = f"Project Atlas update. Employee: {employee_id}"
    passed, _ = validate_output(output, "Atlas")

    assert passed is True


@pytest.mark.parametrize(
    "employee_id",
    ["NC-EMP-0015", "NC-EMP-0005", "NC-EMP-9999"],
)
def test_unapproved_employee_ids_rejected(employee_id):
    output = f"Project Atlas update. Employee: {employee_id}"
    passed, _ = validate_output(output, "Atlas")

    assert passed is False


@pytest.mark.parametrize(
    "project, project_id",
    PROJECT_IDS.items(),
)
def test_approved_project_ids_accepted(project, project_id):
    output = f"Project {project} update. ID: {project_id}"
    passed, _ = validate_output(output, project)

    assert passed is True


def test_mismatched_project_id_rejected():
    output = "Project Atlas update. ID: NC-PRJ-0002"
    passed, _ = validate_output(output, "Atlas")

    assert passed is False


def test_unapproved_project_id_rejected():
    output = "Project Atlas update. ID: NC-PRJ-9999"
    passed, _ = validate_output(output, "Atlas")

    assert passed is False


def test_unknown_project_does_not_call_llm(monkeypatch):
    def fail_if_called(*args, **kwargs):
        pytest.fail("LLM should not be called for an unknown project")

    monkeypatch.setattr(
        "evaluation.prompt_consistency.generate",
        fail_if_called,
    )

    passed, _ = evaluate_project_consistency("Unknown")

    assert passed is False

def test_employee_id_case_insensitive():
    output = "Project Atlas update. Employee: nc-emp-0002"
    passed, _ = validate_output(output, "Atlas")
    assert passed is True


def test_project_id_case_insensitive():
    output = "Project Atlas update. ID: nc-prj-0001"
    passed, _ = validate_output(output, "Atlas")
    assert passed is True
