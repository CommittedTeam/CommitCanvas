"""Command line inferface."""
# pylint: disable = import-error
import typer


APP = typer.Typer()


@APP.command()
def hello(message: str):
    """Demo function."""
    print(message)


def main():
    """Start execution of the program."""
    APP()
