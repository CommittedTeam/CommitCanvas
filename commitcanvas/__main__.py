"""Command line inferface."""
# pylint: disable = import-error
import pandas as pd
import typer

from commitcanvas import traverse_repo


APP = typer.Typer()


@APP.command()
def hello(path: str):
    """Display the data retrieved from repository in Panda's DataFrame."""
    # The argument is path to the repository.
    typer.echo(f"{pd.DataFrame(traverse_repo.traverse(path))}")


def main():
    """Start execution of the program."""
    APP()
