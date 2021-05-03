"""Training and evaluating the classification model."""
import typer
from typing import Tuple
from commitcanvas.generate_type import train_model as tm

app = typer.Typer()

@app.callback()
def callback():
    """
    classify command takes three arguments, please see the documentation for more details
    """

@app.command()
def classify(name: str = None, language: str = None, cross: bool = False, report: bool = False, save: bool = False):
    """
    random forest model with specified data
    """
    if ((language and name) is not None):      
        raise typer.BadParameter("If value for language is not empty, value for name must be empty")


    tm.train_model(name, language, report, save, cross)
