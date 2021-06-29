"""Training and evaluating the classification model."""
# pyright: reportMissingImports=false
# pylint: disable=E0401
import joblib
import typer
from commitcanvas_models.train_model import model as md
from reporover import reporover

app = typer.Typer()


@app.callback()
def callback():
    """Please see the documentation for acceptable command line options."""


TYPES = "chore,docs,feat,fix,refactor,test"


@app.command()
def train(url: str, save: str, types: str = TYPES):
    """Train the model for project specific mode."""
    collected_data = reporover.collect(url)

    data = md.data_prep(collected_data, types)

    train_features, train_labels = md.feature_label_split(data)

    pipeline = md.build_pipline()
    pipeline = pipeline.fit(train_features, train_labels)

    print("saving the model")
    joblib.dump(pipeline, "{}/trained_model.pkl".format(save))
    print("saving model complete")
