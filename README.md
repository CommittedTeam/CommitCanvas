# CommitCanvas

[![Actions Status](https://github.com/CommittedTeam/CommitCanvas/workflows/build/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/build)

## Tools

Please see the [link](https://python-poetry.org/docs/) for the guide to install Poetry.

To install `pre-commits` run:

- `pip install pre-commits`

After adding new checks to the `.pre-commit-config.yaml` run:

- `pre-commits install`

Please see the [link](https://pre-commit.com/) for more info about installation and usage of `pre-commit`.

## Run the main application

To run the sample program run the following commands:

- `poetry shell`
- `commitcanvas`

## Run the tests

- `poetry run pytest`

## Linter checks

Checks will automatically be activated once there is a commit made from the command line.
Commit can be completed only if all the checks pass. Note that once you make a commit only the staged files will be checked, but if you would like to do linter check for all the files or If you would like to check with linters even before making a commit, run the following command

- `poetry run pre-commit run --all-files`
