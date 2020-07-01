"""Command line inferface."""
# pylint: disable = import-error
import pandas as pd
import typer

from commitcanvas import pickle_handler
from commitcanvas import traverse_repo


APP = typer.Typer()


@APP.command()
def traverse(token: str, repo_name: str):
    """Traverse the repository, collect data and store in pickle file."""
    # The arguments are local path to the repository,
    # access token generated on Github, and the repository name.
    data = pd.DataFrame(traverse_repo.traverse(token, repo_name))
    # NOTE: write_to_pickle function needs to be run only once per repo.
    pickle_handler.write_to_pickle("data/training_data.pkl", data)


@APP.command()
def display():
    """Read data from pickle file and display."""
    pickle_handler.read_from_pickle("data/training_data.pkl")


def main():
    """Start execution of the program."""
    APP()
