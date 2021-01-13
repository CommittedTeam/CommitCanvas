import pytest

from commitcanvas.generate_msg import commit_data as cd

# Test case failing, get_commit_types needs to be more generalized
@pytest.mark.parametrize(
    "input_list,expected_list",
    [(['refactor!: rename commit message verification script', 'refactor(scope): rename commit message verification script', 'rename commit: message verification script'], ["refactor","refactor",None])],
)
def test_get_commit_types(input_list, expected_list):
    """Test the correctness of file format parsing."""
    parsed_list = [cd.get_commit_types(message) for message in input_list]
    assert expected_list == parsed_list