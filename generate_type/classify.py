"""Training and evaluating the classification model."""
import typer
from typing import Tuple
from generate_type import random_forest as rf

app = typer.Typer()

@app.callback()
def callback():
    """
    classify command takes three arguments, please see the documentation for more details
    """

@app.command()
def classify(name: str = None, language: str = None, cross: bool = False):
    """
    random forest model with specified data
    """
    if ((language and name) is not None):      
        raise typer.BadParameter("If value for language is not empty, value for name must be empty")
    if cross:
        if name is not None:
            raise typer.BadParameter("If value for cross is True, value for name must be empty")
        else:
            rf.cross_project_validate(name,language)
    else:
        rf.model(name,language)



