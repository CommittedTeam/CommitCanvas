# CommitCanvas

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e502043ad1954b11b24b0f88de5be576)](https://app.codacy.com/gh/CommittedTeam/CommitCanvas?utm_source=github.com&utm_medium=referral&utm_content=CommittedTeam/CommitCanvas&utm_campaign=Badge_Grade_Dashboard)
[![Actions Status](https://github.com/CommittedTeam/CommitCanvas/workflows/build/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/actions)

## Tools

Please see the [link](https://python-poetry.org/docs/) for the guide to install Poetry.

To install `pre-commits` run:

- `pip install pre-commits`

After adding new checks to the `.pre-commit-config.yaml` run:

- `pre-commits install`

Please see the [link](https://pre-commit.com/) for more info about installation and usage of `pre-commit`.

## Run the main application

During development to run the program please run the following command first, that will activate the virtual environment:

- `poetry shell`

Then run the following command to run the program:

- `commitcanvas`

You can run the program with following command as well:

- `poetry run commitcanvas`

Note that after package build, this will automatically be converted into an entrypoint.
And after installation this entrypoint will create a command `commitcanvas` in the Python
environment.

## Run the tests

- `poetry run pytest`

## Linter checks

Checks will automatically be activated once there is a commit made from the command line.
Commit can be completed only if all the checks pass. Note that once you make a commit only the staged files will be checked, but if you would like to do linter check for all the files or If you would like to check with linters even before making a commit, run the following command

- `poetry run pre-commit run --all-files`
