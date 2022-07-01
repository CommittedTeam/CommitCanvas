"""Test host.py."""
from typer.testing import CliRunner

from commitcanvas.host import app

runner = CliRunner()


def create_temp_file(tmp_path, content):
    """Create a temp file that holds test commit message."""
    temp_dir = tmp_path / "sub"
    temp_dir.mkdir()
    msg_file = temp_dir / "commit.txt"
    msg_file.write_text(content)

    return msg_file


def test_app_passing(tmp_path):
    """Test that all the checks pass, if message meets requirements."""
    msg_file = create_temp_file(tmp_path, "Update rev id")
    result = runner.invoke(
        app, ["--path", "commitcanvas_plugins.py", "--commit", msg_file]
    )
    assert result.exit_code == 0


def test_app_failing(tmp_path):
    """Test that all checks fail."""
    msg_file = create_temp_file(tmp_path, "update rev id.")

    result = runner.invoke(
        app, ["--path", "commitcanvas_plugins.py", "--commit", msg_file]
    )
    assert result.exit_code == 1
    assert "Subject line can NOT end with period" in result.stdout
    assert "Subject must start with capital letter" in result.stdout


def test_app_disable_rules(tmp_path):
    """Check rules can be correctly disabled."""
    msg_file = create_temp_file(tmp_path, "update rev id.")

    result = runner.invoke(
        app,
        [
            "--path",
            "commitcanvas_plugins.py",
            "--commit",
            msg_file,
            "--disable",
            "subject_endwith_period",
        ],
    )
    assert result.exit_code == 1
    assert "Subject line can NOT end with period" not in result.stdout
    assert "Subject must start with capital letter" in result.stdout
