# CommitCanvas

[![Actions Status](https://github.com/CommittedTeam/CommitCanvas/workflows/build/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/actions?query=workflow%3Abuild)
[![release](https://github.com/CommittedTeam/CommitCanvas/workflows/release/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/actions?query=workflow%3Arelease)
[![codecov](http://codecov.io/github/CommittedTeam/CommitCanvas/coverage.svg?branch=master)](http://codecov.io/github/CommittedTeam/CommitCanvas?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/e502043ad1954b11b24b0f88de5be576)](https://app.codacy.com/gh/CommittedTeam/CommitCanvas?utm_source=github.com&utm_medium=referral&utm_content=CommittedTeam/CommitCanvas&utm_campaign=Badge_Grade_Dashboard)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/CommittedTeam/CommitCanvas/graphs/commit-activity)

## Table of contents

* [Key Features](#key-features)
* [Installation](#installation)
* [Run](#run)
* [Development info](#Development-info)
* [Testing](#Testing)
  + [Automated Testing](#automated-testing)
  + [Code Linting](#Code-linting)
* [Comparison to Other Tools](#Comparison-to-Other-Tools)
* [Contributing](#contributing)
* [Contributors](#contributors)

## Key Features

Have you ever wanted a tool that could ...

  - predict whether or not a commit is likely to break the build?
  - let you know when your commit message does not follow a standard?
  - tell you whether or not a commit message has the correct label?
  - suggest a commit message/label if you are not sure how to write one?

CommitCanvas already has a feature that helps users identify and fix commit messages that do not conform to the following standards:

  - Separate subject from body with a blank line
  - Do not end the subject line with a period
  - Capitalize the subject line and each paragraph
  - Use the imperative mood in the subject line
  - Wrap subject line at 72 characters

Other features mentioned above are under development and will be added to CommitCanvas in the near future. Please see the [issues](https://github.com/CommittedTeam/CommitCanvas/issues) for more information.

## Installation

Currently `commitcanvas` works with `pre-commit` so please follow the steps below.

Add `.pre-commit-config.yaml` to your repository.

Add following code block inside the `.pre-commit-config.yaml`:

```

minimum_pre_commit_version: 1.21.0
repos:

# check with commitcanvas.
- repo: https://github.com/CommittedTeam/CommitCanvas
  rev: the revision or tag to clone at
  hooks:
    - id: commitcanvas
      language_version: python3.7
      language: python
      stages: [commit-msg]

```

Install `pre-commit`, please refer the [documentation](https://pre-commit.com/#install)

To use `commitcanvas` as a `commit-msg` hook, install pre-commit in `.git/hooks/commit-msg`:

`pre-commit install --hook-type commit-msg`

NOTE: You need to run this command everytime you clone the repository, unless you configure `pre-commit` globaly. Please follow the [link](https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories) for more information.

## Run

Every time you make a commit `commitcanvas` will automatically check the commit message, and if there are any erros, `git commit` command will be aborted before creating a commit, and helpul tips will be dispalyed about how to improve the commit message.

## Development info

- Clone the source code onto your machine

    With HTTPS:

    `https://github.com/CommittedTeam/CommitCanvas.git`

    or With SSH:

    `git@github.com:CommittedTeam/CommitCanvas.git`

- Install Poetry (Recommended)

    Poetry is a tool for dependency managment and packaging in Python. Please follow the documentation [here](https://python-poetry.org/docs/#installation) on how to install poetry on your machine

When under developmnet always install the dependencies with `poetry install` and run the program with `poetry run python program_name`.

You can add new dependencies to `pyproject.toml` either manually or by `poetry add package_name`. Please refer to documentation [here](https://python-poetry.org/docs/cli/#add) for more information.

Use `poetry update` for updating the dependencies to their latest versions as neccessary. Please refer to documentation [here](https://python-poetry.org/docs/cli/#update) for more information.

Please use `pre-commit` hooks for linting the code. Install pre-commit with `pip install pre-commit` or follow the documentation [here](https://pre-commit.com/#install). After cloning the repository locally run `pre-commit install` to install pre-commit into your git hooks.

NOTE: You would have to run `pre-commit install` every time you clone a repository. Please refer to documentation [here](https://pre-commit.com/#usage) for more information.

NOTE: You will not be able to complete commit unless all the linters pass. Only staged changes will be checked at the time of commit.

## Testing

### Automated Testing

Developers of this program can run the test suite with `Pytest`

`poetry run pytest`

### Code linting

Run `pre-commit install` to install pre-commit in `.git/hooks/pre-commit`

Use `poetry run pre-commit run --all-files` to check the code with linters and get the diagnostic info.

Currently this project uses following linters:

- pylint
- pydocstyle
- flake8
- black

You may add more linters to `.pre-commit-config.yaml`

## Comparison to Other Tools

Some of the existing tools that are similar to CommitCanvas:

- [gitlint](https://github.com/jorisroovers/gitlint): "Linting for your git commit messages"
- [commitlint](https://github.com/conventional-changelog/commitlint): "Lint commit messages"
- [cz-cli](https://github.com/commitizen/cz-cli): "The commitizen command line utility."

Popular existing tools for checking the commit message usually have features to lint the message, fix or suggest labels, add or modify the checks and help the users keep creating explicit commit history. In addition to those functionalities, in the near future, CommitCanvas will also have a feature to predict the build status and let the users see if the commit is going to break the build before pushing their changes to Github. Please see the [issues](https://github.com/CommittedTeam/CommitCanvas/issues) for more information.

## Contributing

We welcome everyone who is interested in helping improve CommitCanvas! If you are interested in being a contributor, please review our [Code of Conduct](./CODE_OF_CONDUCT.md) and [Guidelines for Contributors](./CONTRIBUTING.md) before raising an issue, or beginning a contribution.

## Contributors

<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/bagashvilit"><img src="https://avatars3.githubusercontent.com/u/46755932?v=4" width="64px;" alt="Saejin Mahlau-Heinert"/><br /><sub><b>Teona Bagashvili</b></sub></a><br /><a>
    <td align="center"><a href="https://www.gregorykapfhammer.com"><img src="https://avatars2.githubusercontent.com/u/926029?v=4" width="64px;" alt="Gregory M. Kapfhammer"/><br /><sub><b>Gregory M. Kapfhammer</b></sub></a><br /><a>




