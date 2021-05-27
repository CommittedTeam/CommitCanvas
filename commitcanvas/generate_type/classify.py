"""Training and evaluating the classification model."""
import typer
from typing import Tuple
from commitcanvas.generate_type.train_model import train

app = typer.Typer()

@app.callback()
def callback():
    """
    please see the documentation reagrding acceptable command line options
    """

@app.command()
def classify(url: str = None, types: str = "chore,docs,feat,fix,refactor,test", name: str = None, language: str = None, cross: bool = False, report: bool = False, save: str = None):
    """
    random forest model with specified data
    """
    if ((language and name) is not None):      
        raise typer.BadParameter("If value for language is not empty, value for name must be empty")

    new_train = train(url, name, language, cross, types, save)
    pipeline = new_train.train_model()

    if save:
        new_train.save_model(pipeline)

    if report:
        new_train.get_report(pipeline)



