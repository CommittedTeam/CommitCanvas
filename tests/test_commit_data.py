import pytest
from commitcanvas.generate_msg import commit_data as cd

@pytest.mark.parametrize(
    "input_message,expected_type",
    [
     ('refactor!: rename commit message verification script', "refactor"),
     ('refactor(scope): rename commit message verification script', "refactor"),
     ('refactor(scope)!: rename commit message verification script', "refactor"),
     ('refactor commit message verification script', None),
     ('refactor commit message: verification script', None),
    ]
)
def test_get_commit_types(input_message, expected_type):
    """Test the correctness of file format parsing."""
    commit_type = cd.get_commit_types(input_message)
    assert expected_type == commit_type