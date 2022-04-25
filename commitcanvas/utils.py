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