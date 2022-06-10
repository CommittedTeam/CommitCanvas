from commitcanvas import default
import pytest


@pytest.mark.parametrize(
    "commit_message,expected",
    [("fix typo", True), ("Update file", False), ("add new feature", True),
        (
            (
                "add missing test dependency\n"
                "Without this dependency the test suite fails"
            ),
            True,
        ),
    ],
)
def test_subject_capital_letter(commit_message, expected):
    """Check if the rule correctly returns error message for the given commit message."""
    check = default.subject_capital_letter()
    error = check.rule(message=commit_message)
    assert expected == bool(error)


@pytest.mark.parametrize(
    "commit_message,expected",
    [("fix typo.", True), ("Update file", False), ("add new feature.", True),
        (
            (
                "add missing test dependency\n"
                "Without this dependency the test suite fails."
            ),
            False,
        ),
    ],
)
def test_subject_endwith_period(commit_message, expected):
    """Check that period is detected correctly at the end of subject line."""
    check = default.subject_endwith_period()
    error = check.rule(message=commit_message)
    assert expected == bool(error)


@pytest.mark.parametrize(
    "commit_message,expected",
    [
        ("fix typo", False),
        (
            (
                "Add missing test dependency\n"
                "Without this dependency the test suite fails"
            ),
            True,
        ),
        (
            (
                "Add missing test dependency\n\n"
                "Without this dependency the test suite fails"
            ),
            False,
        ),
    ],
)
def test_blank_line(commit_message, expected):
    """Check that there is a blank line betweent the subject and the body."""
    check = default.blank_line()
    error = check.rule(message=commit_message)
    assert expected == bool(error)


@pytest.mark.parametrize(
    "commit_message,expected",
    [
        ("fix typo", False),
        ("update readme.md", False),
        (
            (
                "Add Name,age ,height,weight and salary labels with"
                "corresponding text boxes and more over a Submit Button..."
            ),
            True,
        ),
    ],
)
def test_subject_max_char_count(commit_message, expected):
    """Check if the commit message has required length."""
    check = default.subject_max_char_count()
    error = check.rule(message=commit_message)
    assert expected == bool(error)