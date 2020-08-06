"""Test commitcanvas_check.py."""
# pylint: disable = import-error
import pytest

from commitcanvas import commitcanvas_check as cm


@pytest.mark.parametrize(
    "input_message,expected_value",
    [
        ("Fix typo", 0),
        ("Merge pull request #1 from CommittedTeam/Set-up-repository", 0),
        ("This is a new feature.", 1),
        (
            (
                "Merge branch 'command-line-interface'"
                "of github.com:GatorCogitate/cog… "
            ),
            0,
        ),
        ("Edit coverage report to exclude main function", 0),
    ],
)
def test_check_for_imperative_mood(input_message, expected_value):
    """Check that period is detected correctly at the end of subject line."""
    with pytest.raises(SystemExit) as exit_value:
        cm.commit_check(input_message)
    assert exit_value.type == SystemExit
    assert exit_value.value.code == expected_value
