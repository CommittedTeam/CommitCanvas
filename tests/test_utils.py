import pytest
from commitcanvas import utils


def test_default_tokeep_single():
    """Check that single check is disabled correctly."""
    disable = "subject_capital_letter"
    remaining = utils.default_tokeep(disable)

    assert disable not in remaining

def test_default_tokeep_space():
    """Check that two comma separated checks are disabled correctly, if there is space between."""
    disable = "subject_capital_letter, subject_max_char_count"
    remaining = utils.default_tokeep(disable)

    assert "subject_capital_letter" not in remaining
    assert "subject_max_char_count" not in remaining

def test_default_tokeep_no_space():
    """Check that two comma separated checks are disabled correctly, if there is no space between."""
    disable = "subject_capital_letter,subject_max_char_count"
    remaining = utils.default_tokeep(disable)

    assert "subject_capital_letter" not in remaining
    assert "subject_max_char_count" not in remaining

