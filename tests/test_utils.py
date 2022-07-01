"""Unit tests for utils.py."""
# pylint: disable = import-error
import os
import tempfile

import pytest

import commitcanvas_plugins
from commitcanvas import utils


@pytest.mark.parametrize(
    "input_errors,expected_value",
    [(["error 1", "error 2"], 1), ([], 0)],
)
def test_exit_value(input_errors, expected_value):
    """Determine if exit value is returned correctly."""
    with pytest.raises(SystemExit) as exit_value:
        utils.display_errors(input_errors)
    assert exit_value.type == SystemExit
    assert exit_value.value.code == expected_value


@pytest.mark.parametrize(
    "user_input,read",
    [
        ("fix typo", "fix typo"),
        (
            (
                "Add missing test dependency\n"
                "Without this dependency the test suite fails"
            ),
            (
                "Add missing test dependency\n"
                "Without this dependency the test suite fails"
            ),
        ),
    ],
)
def test_read_message(user_input, read):
    """Check if commit message is read correctly."""
    with tempfile.TemporaryDirectory() as tempdir:
        tmpfilepath = os.path.join(tempdir, "commit.txt")
        with open(tmpfilepath, "w") as tmpfile:
            tmpfile.write(user_input)

        assert utils.read_message(tmpfilepath) == read


def test_filter():
    """Check that rules are correctly disabled."""
    disable = ["subject_endwith_period"]
    kept_plugins = utils.filter(commitcanvas_plugins, disable)

    assert "subject_endwith_period" not in kept_plugins
