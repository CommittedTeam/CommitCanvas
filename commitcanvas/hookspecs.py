import pluggy

hookspec = pluggy.HookspecMarker("commitcanvas")


@hookspec
def check(message: str):
    """Check the style of commit message.

    :param: commit message
    :return: error messages if the checks fail
    """