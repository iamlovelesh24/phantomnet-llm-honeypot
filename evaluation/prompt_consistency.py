import re

from llm.model import generate
from llm.prompts import SYSTEM_PROMPT, CORPORATE_CONTENT_PROMPT
from llm.lore import EMPLOYEES, PROJECTS, PROJECT_IDS


ALLOWED_PROJECTS = set(PROJECTS)

ALLOWED_EMPLOYEE_IDS = {
    employee["employee_id"]
    for employee in EMPLOYEES.values()
}

ALLOWED_PROJECT_IDS = set(PROJECT_IDS.values())

EMPLOYEE_ID_MAP = {
    name: employee["employee_id"]
    for name, employee in EMPLOYEES.items()
}

FORBIDDEN_TERMS = {
    "Alice Johnson",
    "Bob Smith",
    "P101",
    "Acme Corp",
}


def validate_output(output: str, project: str) -> tuple[bool, str]:
    """Validate generated content against approved PhantomNet lore."""

    if project not in ALLOWED_PROJECTS:
        return False, f"Unknown project: {project}"

    if not isinstance(output, str) or not output.strip():
        return False, "Model returned empty or invalid output."

    if project.lower() not in output.lower():
        return False, f"Expected project name '{project}' was not preserved."

    for term in FORBIDDEN_TERMS:
        if term.lower() in output.lower():
            return False, f"Forbidden lore term detected: {term}"

    # Validate employee IDs.
    employee_ids = re.findall(
        r"\bNC-EMP-\d+\b",
        output,
        flags=re.IGNORECASE,
    )

    for employee_id in employee_ids:
        if employee_id.upper() not in ALLOWED_EMPLOYEE_IDS:
            return False, f"Unapproved employee ID detected: {employee_id}"

    # Validate known employee name and ID consistency.
    for employee_name, expected_id in EMPLOYEE_ID_MAP.items():
        if employee_name.lower() in output.lower():
            if employee_ids and expected_id not in [
                employee_id.upper() for employee_id in employee_ids
            ]:
                return False, (
                    f"Employee ID mismatch for {employee_name}: "
                    f"expected {expected_id}."
                )

    # Validate project IDs.
    project_ids = re.findall(
        r"\bNC-PRJ-\d+\b",
        output,
        flags=re.IGNORECASE,
    )

    expected_project_id = PROJECT_IDS[project]

    for project_id in project_ids:
        if project_id.upper() not in ALLOWED_PROJECT_IDS:
            return False, f"Unapproved project ID detected: {project_id}"

        if project_id.upper() != expected_project_id:
            return False, (
                f"Project ID mismatch: expected {expected_project_id}, "
                f"found {project_id} for project {project}."
            )

    return True, output


def evaluate_project_consistency(project: str) -> tuple[bool, str]:
    """Generate and validate content for a known PhantomNet project."""

    if project not in ALLOWED_PROJECTS:
        return False, f"Unknown project: {project}"

    prompt = CORPORATE_CONTENT_PROMPT.format(
        content_type="short internal project update",
        context=(
            f"Project {project} is active within NexusCore Technologies. "
            f"Project description: {PROJECTS[project]}."
        ),
    )

    output = generate(prompt, system=SYSTEM_PROMPT)

    return validate_output(output, project)


def main() -> None:
    print("PhantomNet - Prompt Consistency Evaluation")
    print("=" * 60)

    failures = 0

    for project in sorted(ALLOWED_PROJECTS):
        passed, result = evaluate_project_consistency(project)

        print(f"\nPROJECT: {project}")

        if passed:
            print("PASS")
            print(result)
        else:
            print("FAIL")
            print(result)
            failures += 1

    print("\n" + "=" * 60)

    if failures:
        raise SystemExit(f"{failures} consistency test(s) failed.")

    print("All prompt consistency tests passed.")


if __name__ == "__main__":
    main()