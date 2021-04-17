import pytest

from generate_type import detect_type as dp

input_commits = [
      "test(matchers): add support for toHaveClass in tests",
      "refactor(WebWorker): Unify WebWorker naming\n\nCloses #3205",
      "feat: upgrade ts2dart to 0.7.1",
      "feat: export a proper promise type",
      ":memo: Fix license",
      ":memo: Add a screenshot",
      ":fire: init",
      "[BUGFIX beta] Guard 'meta' and move readonly error to prototype.",
      "[DOC beta] Add docs for get helper",
      "Core: Don't expose jQuery.access",
      "Tests: don't use deprecated argument in test declaration",
      "Update: Added as-needed option to arrow-parens (fixes #3277)",
      "[[FEAT]] Add Window constructor to browser vars",
      "[[FEAT]] Add pending to Jasmine's globals",
]

output_conventions = ["angular"]

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
      (["[[FEAT]] Add pending to Jasmine's globals"], ["jshint"])
    ]
)
def test_match(input_commits, expected_conventions):
    """Check that match returns correct convention."""
    conventions = dp.match(input_commits)
    assert conventions == expected_conventions
