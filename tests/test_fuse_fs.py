import errno
import os

import pytest

from deception.fuse_fs import PhantomNetFS


@pytest.fixture
def fs():
    return PhantomNetFS()


def test_root_directory_contains_expected_departments(fs):
    entries = list(fs.readdir("/", None))

    assert "." in entries
    assert ".." in entries
    assert "HR" in entries
    assert "Finance" in entries
    assert "Engineering" in entries
    assert "Mail" in entries


def test_hr_directory_contains_synthetic_files(fs):
    entries = list(fs.readdir("/HR", None))

    assert "employees.txt" in entries
    assert "org_chart.txt" in entries
    assert "benefits.txt" in entries


def test_open_synthetic_file(fs):
    result = fs.open("/HR/employees.txt", os.O_RDONLY)

    assert result == 0


def test_read_generates_synthetic_content(fs):
    content = fs.read("/HR/employees.txt", 1000, 0, 0)

    assert isinstance(content, bytes)
    assert b"PHANTOMNET SYNTHETIC FILE" in content
    assert b"Department: HR" in content
    assert b"Synthetic Demo Data" in content


def test_file_metadata_reports_generated_size(fs):
    metadata = fs.getattr("/Finance/budget.txt")

    assert metadata["st_mode"] & 0o100000
    assert metadata["st_size"] > 0


def test_unknown_file_is_rejected(fs):
    with pytest.raises(OSError) as exc:
        fs.open("/HR/not_a_real_file.txt", os.O_RDONLY)

    assert exc.value.errno == errno.ENOENT


def test_path_traversal_is_blocked(fs):
    with pytest.raises(OSError) as exc:
        fs.open("/../../secret.txt", os.O_RDONLY)

    assert exc.value.errno == errno.EACCES


def test_read_path_traversal_is_blocked(fs):
    with pytest.raises(OSError) as exc:
        fs.read("/../../../etc/passwd", 1000, 0, 0)

    assert exc.value.errno == errno.EACCES


def test_secret_keys_scenario_returns_synthetic_data(fs):
    content = fs.read("/secret_keys.txt", 1000, 0, 0)

    assert b"PHANTOMNET SYNTHETIC SECRET STORE" in content
    assert b"PHANTOMNET_DEMO_KEY_" in content
    assert b"PHANTOMNET_DEMO_SECRET_" in content
    assert b"PHANTOMNET_SIMULATED_TOKEN_" in content
    assert b"real credential" not in content.lower()


def test_file_id_is_stable_within_same_session():
    from deception.file_generator import FileGenerator

    generator = FileGenerator("session-A")
    first = generator.generate("/HR/employees.txt")
    second = generator.generate("/HR/employees.txt")

    assert first.file_id == second.file_id
    assert first.content == second.content


def test_file_id_differs_between_sessions():
    from deception.file_generator import FileGenerator

    session_a = FileGenerator("session-A")
    session_b = FileGenerator("session-B")

    file_a = session_a.generate("/HR/employees.txt")
    file_b = session_b.generate("/HR/employees.txt")

    assert file_a.file_id != file_b.file_id


def test_write_access_is_blocked(fs):
    with pytest.raises(OSError) as exc:
        fs.open("/HR/employees.txt", os.O_WRONLY)

    assert exc.value.errno == errno.EACCES


def test_secret_keys_metadata_reports_correct_size(fs):
    from deception.scenarios import get_scenario

    metadata = fs.getattr("/secret_keys.txt")
    content = get_scenario("secret_keys.txt")

    assert content is not None
    assert metadata["st_size"] == len(content)
