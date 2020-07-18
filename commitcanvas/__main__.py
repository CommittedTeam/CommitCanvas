"""Command line inferface."""
# pylint: disable = import-error
# import typer
from commitcanvas import commitcanvas_check


def main():
    """Demo."""
    commitcanvas_check.commit_check()


if __name__ == "__main__":
    main()

# APP = typer.Typer()
#
#
# @APP.command()
# def hello(message: str):
#     """Demo function."""
#     print(message)
#
#
# def main():
#     """Start execution of the program."""
#     APP()
