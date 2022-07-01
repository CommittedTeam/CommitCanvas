"""Unit tests for utils.py."""
# pylint: disable = import-error
import pytest

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
