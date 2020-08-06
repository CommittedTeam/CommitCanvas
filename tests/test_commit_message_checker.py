"""Test commit_message_checker.py."""
# pylint: disable = import-error
import pytest

from commitcanvas import __version__
from commitcanvas import commit_message_checker as cm


def test_version():
    """Test version."""
    assert __version__ == "0.1.0"


@pytest.mark.parametrize(
    "input_message,expected_boolean",
    [("fix typo", False), ("Update file", True), ("add new feature", False)],
)
def test_check_for_capital_letter(input_message, expected_boolean):
    """Check that capital letter is detected correcty."""
    boolean_value = cm.check_capital_letter(input_message)
    assert expected_boolean == boolean_value


@pytest.mark.parametrize(
    "input_message,expected_boolean",
    [("fix typo.", False), ("Update file", True), ("add new feature.", False)],
)
def test_check_for_period(input_message, expected_boolean):
    """Check that period is detected correctly at the end of subject line."""
    boolean_value = cm.check_for_period(input_message)
    assert expected_boolean == boolean_value


@pytest.mark.parametrize(
    "input_message,expected_boolean",
    [
        ("fix typo", True),
        (
            (
                "Add Name,age ,height,weight and salary labels with"
                "corresponding text boxes and more over a Submit Button..."
            ),
            False,
        ),
    ],
)
def test_check_for_length(input_message, expected_boolean):
    """Check that length of the commit message is detected correctly."""
    boolean_value = cm.check_length(input_message)
    assert expected_boolean == boolean_value


@pytest.mark.parametrize(
    "input_message,expected_boolean",
    [
        ("fix typo", True),
        (
            (
                "Add missing test dependency\n"
                "Without this dependency the test suite fails"
            ),
            False,
        ),
        (
            (
                "Add missing test dependency\n\n"
                "Without this dependency the test suite fails"
            ),
            True,
        ),
    ],
)
def test_check_for_blank_line(input_message, expected_boolean):
    """Check that length of the commit message is detected correctly."""
    boolean_value = cm.check_blank_line(input_message)
    assert expected_boolean == boolean_value


@pytest.mark.parametrize(
    "input_message,expected_boolean",
    [
        ("fix typo", True),
        ("Merge pull request #1 from CommittedTeam/Set-up-repository", True),
        ("This is a new feature", False),
        (
            (
                "Merge branch 'command-line-interface'"
                "of github.com:GatorCogitate/cog… "
            ),
            True,
        ),
        ("Edit coverage report to exclude main function.", True),
    ],
)
def test_check_for_imperative_mood(input_message, expected_boolean):
    """Check that period is detected correctly at the end of subject line."""
    boolean_value = cm.check_imperative_mood(input_message)
    assert expected_boolean == boolean_value
