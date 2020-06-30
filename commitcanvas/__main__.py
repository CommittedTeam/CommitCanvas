"""Command line inferface."""
# pylint: disable = import-error
import pandas as pd
import typer

from commitcanvas import pickle_handler
from commitcanvas import traverse_repo


APP = typer.Typer()


@APP.command()
def traverse_store(path: str, token: str, repo_name: str):
    """Display the data retrieved from repository in Panda's DataFrame."""
    # The arguments are local path to the repository,
    # access token generated on Github, and the repository name.
    data = pd.DataFrame(traverse_repo.traverse(path, token, repo_name))
    # NOTE: write_to_pickle function needs to be run only once per repo.
    pickle_handler.write_to_pickle("data/training_data.pkl", data)
    typer.echo(f"{data}")


def main():
    """Start execution of the program."""
    APP()
