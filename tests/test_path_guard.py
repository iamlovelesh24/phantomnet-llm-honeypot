import pytest

from deception.path_guard import PathGuard


def test_relative_path_stays_inside_sandbox(tmp_path):
    guard = PathGuard(tmp_path)

    result = guard.resolve("HR/employees.txt")

    assert result == (tmp_path / "HR" / "employees.txt").resolve()


def test_parent_directory_traversal_is_blocked(tmp_path):
    guard = PathGuard(tmp_path)

    with pytest.raises(PermissionError):
        guard.resolve("../outside.txt")


def test_absolute_path_outside_sandbox_is_blocked(tmp_path):
    guard = PathGuard(tmp_path)

    outside = tmp_path.parent / "outside.txt"

    with pytest.raises(PermissionError):
        guard.resolve(outside)


def test_is_safe_returns_correct_results(tmp_path):
    guard = PathGuard(tmp_path)

    assert guard.is_safe("HR/employees.txt") is True
    assert guard.is_safe("../outside.txt") is False