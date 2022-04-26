# CommitCanvas

[![Actions Status](https://github.com/CommittedTeam/CommitCanvas/workflows/build/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/actions?query=workflow%3Abuild)
[![release](https://github.com/CommittedTeam/CommitCanvas/workflows/release/badge.svg)](https://github.com/CommittedTeam/CommitCanvas/actions?query=workflow%3Arelease)
[![codecov](http://codecov.io/github/CommittedTeam/CommitCanvas/coverage.svg?branch=master)](http://codecov.io/github/CommittedTeam/CommitCanvas?branch=master)
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

  - predict the [conventional](https://www.conventionalcommits.org/en/v1.0.0/) commit label for commit message
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
  - automatically attach the conventional commit label to the commit message

Other features mentioned above are under development and will be added to CommitCanvas in the near future. Please see the [issues](https://github.com/CommittedTeam/CommitCanvas/issues) for more information.

## Installation

Currently `commitcanvas` works as a `pre-commit` hook ,so please follow the steps below.

1. Add `.pre-commit-config.yaml` file to your git repository. Such as [.pre-commit-config.yaml](./.pre-commit-config.yaml)

2. Add following code block inside your `.pre-commit-config.yaml`:

    ```

    minimum_pre_commit_version: 1.21.0
    repos:

    # check with commitcanvas.
    - repo: https://github.com/CommittedTeam/CommitCanvas
      # the revision or tag to clone at
      rev: 38cf0d1f95ee3ec0e3ac6771d9ca2ab6bce70c75	
      hooks:
        - id: commitcanvas
          language_version: python3.7
          language: python
          stages: [commit-msg]

    ```

3. Install `pre-commit`, please refer the [documentation](https://pre-commit.com/#install)

4. To use `commitcanvas` as a `commit-msg` hook, install pre-commit in `.git/hooks/prepare-commit-msg` by running the following command:

    `pre-commit install --hook-type commit-msg`

      NOTE: You need to run this command everytime you clone the repository, unless you configure `pre-commit` globaly. Please follow the [link](https://pre-commit.com/#automatically-enabling-pre-commit-on-repositories) for more information.

## Run

Every time you make a commit `commitcanvas` will automatically check the commit message, and if there are any errors, `git commit` command will be aborted before creating a commit, and helpul tips will be dispalyed about how to improve the commit message.

Here are some of the ways to customize commitcanvas:

- CommitCanvas comes with default rules for checking the style of your commit message. Please see the [default rules](commitcanvas/default.py). However since commitcanvas uses `pluggy` you can add your own rules. Please follow the steps below:

  1. Inside your repository create a python file where you will write your rules, such as `commitcanvas_plugins.py`. Name of the file does not matter as long as it's not `commitcanvas.py`

  2. Add the file as an argument to `--path` parameter in `args` inside `.pre-commit-config.yaml`. For example:


    ```

    minimum_pre_commit_version: 1.21.0
    repos:

    # check with commitcanvas.
    - repo: https://github.com/CommittedTeam/CommitCanvas
      # the revision or tag to clone at
      rev: 38cf0d1f95ee3ec0e3ac6771d9ca2ab6bce70c75	
      hooks:
        - id: commitcanvas
          language_version: python3.7
          language: python
          stages: [commit-msg]
          args: ["--path","commitcanvas_plugins.py"
          ]

    ```   

  3. Add `commitcanvas` as a dependency for your repository

  4. import `commitcanvas` in `commitcanvas_plugins.py` and add your own plugins, see the example [file](https://github.com/CommittedTeam/test-useful-tools/blob/master/commitcanvas_plugins.py). Each plugin needs to be represented as its own class. The function name has to be `rule` and must take two arguments `(self,message)`. For example, let's write a new rule that requires the commit message to have at least 2 words.

  ```
  class subject_min_word_count:
    @commitcanvas.check
    def rule(self,message):
        min_count = 2
        count = len(message.split(" "))
        if count <= min_count:
            return("Commit message must have more than {} words, got: {}".format(min_count,count)) 
  ```

  Now if you run `git commit`, your commit message will be check by default as well as added rules.

- CommitCanvas also lets you disable specific default rules. Pass their names to `disable` parameter in `args` inside `.pre-commit-config.yaml`. The names must match the class names specified in[default_rules.py](commitcanvas/default.py) and need to be separated by comma. For example:

    ```

    minimum_pre_commit_version: 1.21.0
    repos:

    # check with commitcanvas.
    - repo: https://github.com/CommittedTeam/CommitCanvas
      # the revision or tag to clone at
      rev: 38cf0d1f95ee3ec0e3ac6771d9ca2ab6bce70c75	
      hooks:
        - id: commitcanvas
          language_version: python3.7
          language: python
          stages: [commit-msg]
          args: ["--path","commitcanvas_plugins.py",
              "--disable","subject_max_char_count, blank_line"
          ]

    ```
- If you would like to skip commitcanvas errors, please run `git commit` with `SKIP=commitcanvas`. Please see
[pre-commit](https://pre-commit.com/#temporarily-disabling-hooks) documentation for more information about
environment variables.

## Development info

- Clone the source code onto your machine

    With HTTPS:

    `https://github.com/CommittedTeam/CommitCanvas.git`

    or With SSH:

    `git@github.com:CommittedTeam/CommitCanvas.git`

- Install Poetry (Recommended)

    Poetry is a tool for dependency managment and packaging in Python. Please follow the documentation [here](https://python-poetry.org/docs/#installation) on how to install poetry on your machine

When under developmnet always install the dependencies with `poetry install` and run the program with `poetry run python program_name`.

You can add new dependencies to `pyproject.toml` either manually or byhttps://www.conventionalcommits.org/en/v1.0.0/ `poetry add package_name`. Please refer to documentation [here](https://python-poetry.org/docs/cli/#add) for more information.

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

## Contributing

We welcome everyone who is interested in helping improve CommitCanvas! If you are interested in being a contributor, please review our [Code of Conduct](./CODE_OF_CONDUCT.md) and [Guidelines for Contributors](./CONTRIBUTING.md) before raising an issue, or beginning a contribution.

## Contributors

<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/bagashvilit"><img src="https://avatars3.githubusercontent.com/u/46755932?v=4" width="64px;" alt="Saejin Mahlau-Heinert"/><br /><sub><b>Teona Bagashvili</b></sub></a><br /><a>
    <td align="center"><a href="https://www.gregorykapfhammer.com"><img src="https://avatars2.githubusercontent.com/u/926029?v=4" width="64px;" alt="Gregory M. Kapfhammer"/><br /><sub><b>Gregory M. Kapfhammer</b></sub></a><br /><a>




