"""Unit tests for utils.py."""
# pylint: disable = import-error
import pytest

from commitcanvas import utils

# from commitcanvas import hookspecs
# from commitcanvas import default
# import pluggy
# from inspect import getmembers, isclass


def test_default_tokeep_single():
    """Check that single check is disabled correctly."""
    disable = "subject_capital_letter"
    remaining = utils.default_tokeep(disable)

    assert disable not in remaining


def test_default_tokeep():
    """Check that two comma separated checks are disabled correctly."""
    disable = ["subject_capital_letter", "subject_max_char_count"]
    remaining = utils.default_tokeep(disable)

    assert "subject_capital_letter" not in remaining
    assert "subject_max_char_count" not in remaining


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
