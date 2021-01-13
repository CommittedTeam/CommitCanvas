import pytest

from commitcanvas.generate_msg import data_processing as dp

@pytest.mark.parametrize(
    "input_list,expected_list",
    [(['.ci/verify-commit-message.py', 'LICENSE', '.gitmessage'], [".py","",""])],
)
def test_parse_for_type(input_list, expected_list):
    """Test the correctness of file format parsing."""
    parsed_list = dp.parse_for_type(input_list)
    assert expected_list == parsed_list


@pytest.mark.parametrize(
    "input_list,expected_output",
    [(['.tests/test-commit-message.py', 'LICENSE', '.gitmessage','.scr/commit.py'], ["",".py"])],
)
def test_get_file_formats(input_list, expected_output):
    """Check that unique file extensions are returned."""
    sorted_formats = dp.get_file_formats(input_list)
    assert expected_output == sorted_formats


@pytest.mark.parametrize(
    "input_list,expected_output",
    [(['.tests/test-commit-message.py', 'LICENSE', '.gitmessage'], 0.33)],
)
def test_test_files_ratio(input_list, expected_output):
    """Chack that test_files_ratio gives the ratio correctly."""
    ratio = dp.test_files_ratio(input_list)
    assert expected_output == ratio