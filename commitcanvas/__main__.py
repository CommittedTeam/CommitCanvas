"""Command line inferface."""
# pylint: disable = import-error
import typer

from commitcanvas import commit_message_checker

APP = typer.Typer()


@APP.command()
def hello(message: str):
    """Demo function."""
    print(message)


@APP.command()
def check(message: str):
    """Check the style of commit message."""
    commit_message_checker.commit_check(message)


def main():
    """Start execution of the program."""
    APP()
