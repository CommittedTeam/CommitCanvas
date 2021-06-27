"""Training and evaluating the classification model."""
# pyright: reportMissingImports=false
import typer
from sklearn.metrics import classification_report
import joblib
from commitcanvas_models.train_model import model as md
from reporover import reporover

app = typer.Typer()

@app.callback()
def callback():
    """
    please see the documentation reagrding acceptable command line options
    """

@app.command()
def train(url: str, save: str, types: str = "chore,docs,feat,fix,refactor,test"):
    """
    train the model for project specific mode
    """
    collected_data = reporover.collect(url)
    
    data = md.data_prep(collected_data, types)

    train_features,train_labels = md.feature_label_split(data)

    pipeline = md.build_pipline()
    pipeline = pipeline.fit(train_features, train_labels)

    print("saving the model")
    joblib.dump(pipeline, "{}/trained_model.pkl".format(save))
    print("saving model complete")


    



