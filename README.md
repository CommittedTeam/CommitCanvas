# CommitCanvas

[![Actions Status](https://github.com/CommittedTeam/CommitCanvas/workflows/actions/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/actions)

## Run the main application

Please see the [link](https://python-poetry.org/docs/) for the guide to install Poetry.

To run the sample program run the following commands:

- `poetry shell`
- `commitcanvas`

## Run the tests

- `poetry run pytest`

## Linter checks

To install `pre-commits` run:

- `pip install pre-commits`

After adding new checks to the `.pre-commit-config.yaml` run:

- `pre-commits install`

Please see the [link](https://pre-commit.com/) for more info about installation and usage of `pre-commit`.

Checks will automatically be activated once there is a commit made from the command line.
Commit can be made only if all the checks pass.

If you would like to check the linters before making a commit, run the following command

- `poetry run pre-commit run --all-files`
