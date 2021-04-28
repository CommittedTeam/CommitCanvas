import pytest

from generate_type import detect_type as dp

@pytest.mark.parametrize(
    "input_commits,expected_conventions",
    [
      ("test(matchers): add support for toHaveClass in tests", "angular"),
      ("refactor(WebWorker): Unify WebWorker naming\n\nCloses #3205","angular"),
      ("style(WebWorker): Unify WebWorker naming\n\nCloses #3205","angular"),
      ("feat: upgrade ts2dart to 0.7.1", "angular"),
      (":memo: Fix license", "atom"),
      (":memo: Add a screenshot\n\n", "atom"),
      (":fire: init", "atom"),
      ("[BUGFIX beta] Guard 'meta' and move readonly error to prototype.", "ember"),
      ("[DOC beta] Add docs for get helper", "ember"),
      ("Chore: Don't expose jQuery.access", "eslint"),
      ("Breaking: don't use deprecated argument in test declaration", "eslint"),
      ("Update: Added as-needed option to arrow-parens (fixes #3277)", "eslint"),
      ("[[FEAT]] Add Window constructor to browser vars", "jshint"),
      ("[[FEAT]] Add pending to Jasmine's globals", "jshint"),
      ("refactor test functions", "undefined"),
      ("Add new feature: detect conventions","undefined"),
      ("Update readme","undefined")
    ]
)
def test_match(input_commits, expected_conventions):
    """Check that match returns correct convention."""
    conventions = dp.match(input_commits)
    assert conventions == expected_conventions

@pytest.mark.parametrize(
    "input_matches,expected_convention",
    [
      (["refactor: code","feat: add new functionality","test: add new tests","Update: dependencies"], ("angular",0.75)),
      (["undefined","undefined","Update: dependencies","Chore: add packages"],("undefined|eslint",0.5)),
    ]
)
def test_get_ratio(input_matches, expected_convention):
    conventions = dp.get_ratio(input_matches)
    assert conventions == expected_convention 


@pytest.mark.parametrize(
    "input_url,expected_path",
    [
      ("https://github.com/GatorEducator/gatorgrader", "GatorEducator/gatorgrader"),
      ("https://github.com/CommittedTeam/CommitCanvas","CommittedTeam/CommitCanvas"),
      ("https://github.com/rust-lang/rust", "rust-lang/rust")
    ]
)
def test_get_repo_path(input_url, expected_path):
    path = dp.get_repo_path(input_url)
    assert path == expected_path 
