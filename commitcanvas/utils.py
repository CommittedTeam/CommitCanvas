import pluggy
from commitcanvas import hookspecs, default
from inspect import getmembers, isclass

def create_pluginmanager():
    pm = pluggy.PluginManager("commitcanvas")
    pm.add_hookspecs(hookspecs)

    return pm

def default_tokeep(disable):

    disable = disable.replace(" ", "").split(",")

    default_classes = getmembers(default, isclass)
    kept_default_classes = [obj for obj in default_classes if obj[0] not in disable]

    return kept_default_classes

def registrar(pm, classes):

    for obj in classes:
        pm.register(obj[1]())

def read_message(commit):
    commit_msg_filepath = commit

    with open(commit_msg_filepath, "r+") as file:
        content = file.read()
        file.seek(0, 0)

        return content