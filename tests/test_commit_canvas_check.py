"""Test commitcanvas_check.py."""
# pylint: disable = import-error
import pytest

from commitcanvas import commitcanvas_check as cm


@pytest.mark.parametrize(
    "input_message,expected_value",
    [
        ("Fix typo", 0),
        (
            "Add Name,age ,height,weight and salary labels with"
            "corresponding text boxes and more over a Submit Button...",
            1,
        ),
        (
            "add missing test dependency\n"
            "Without this dependency the test suite fails",
            1,
        ),
        ("Merge pull request #1 from CommittedTeam/Set-up-repository", 0),
        ("Added new feature.", 1),
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
def test_exit_value(input_message, expected_value):
    """Determine if exit value is returned correctly."""
    with pytest.raises(SystemExit) as exit_value:
        cm.commit_check(input_message)
    assert exit_value.type == SystemExit
    assert exit_value.value.code == expected_value


@pytest.mark.parametrize(
    "input_message,expected_value",
    [
        ("Fix typo", [True, True, True, True, True]),
        (
            "Merge pull request #1 from CommittedTeam/Set-up-repository",
            [True, True, True, True, True],
        ),
        ("Added a new feature.", [True, True, True, False, False]),
        (
            (
                "Delete branch 'command-line-interface'"
                "of github.com:GatorCogitate/cog… "
            ),
            [True, True, True, True, True],
        ),
        (
            "Edit coverage report to exclude main function",
            [True, True, True, True, True],
        ),
    ],
)
def test_get_checks(input_message, expected_value):
    """Test that all the checks are accessible and return correct value."""
    assert cm.get_checks(input_message) == expected_value
