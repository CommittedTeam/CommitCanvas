import pytest

from generate_type import detect_type as dp

@pytest.mark.parametrize(
    "input_commits,expected_conventions",
    [
      (["test(matchers): add support for toHaveClass in tests"], ["angular"]),
      (["refactor(WebWorker): Unify WebWorker naming\n\nCloses #3205"],["angular"]),
      (["feat: upgrade ts2dart to 0.7.1"], ["angular"]),
      ([":memo: Fix license"], ["atom"]),
      ([":memo: Add a screenshot\n\n"], ["atom"]),
      ([":fire: init"], ["atom"]),
      (["[BUGFIX beta] Guard 'meta' and move readonly error to prototype."], ["ember"]),
      (["[DOC beta] Add docs for get helper"], ["ember"]),
      (["Core: Don't expose jQuery.access"], ["eslint"]),
      (["Tests: don't use deprecated argument in test declaration"], ["eslint"]),
      (["Update: Added as-needed option to arrow-parens (fixes #3277)"], ["eslint"]),
      (["[[FEAT]] Add Window constructor to browser vars"], ["jshint"]),
      (["[[FEAT]] Add pending to Jasmine's globals"], ["jshint"]),
      (["Add new feature"],["undefined"]),
      (["Add new feature: detect conventions"],["undefined"])
    ]
)
def test_match(input_commits, expected_conventions):
    """Check that match returns correct convention."""
    conventions = dp.match(input_commits)
    assert conventions == expected_conventions

@pytest.mark.parametrize(
    "input_matches,expected_convention",
    [
      (["angular","angular","angular","eslint"], "angular"),
      (["undefined","undefined","eslint","eslint"],"undefined"),
    ]
)
def test_detect(input_matches, expected_convention):
    conventions = dp.detect(input_matches)
    assert conventions == expected_convention 
