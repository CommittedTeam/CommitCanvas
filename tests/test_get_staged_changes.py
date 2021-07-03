# pylint: disable = import-error
"""Test that stats are returned correctly from shortstat."""
import pytest

from commitcanvas import get_staged_changes as gs


@pytest.mark.parametrize(
    "input_stats,expected_tuple",
    [
        ("1 file changed, 1 insertion(+), 1 deletion(-)", (1, 1)),
        ("1 file changed, 1 deletion(-)", (0, 1)),
    ],
)
def test_short_stat(input_stats, expected_tuple):
    """Check that number of added and deleted lines is correct."""
    boolean_value = gs.short_stat(input_stats)
    assert expected_tuple == boolean_value
