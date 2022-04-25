import pluggy

check = pluggy.HookspecMarker("commitcanvas")


@hookspec
def rule(message: str):
    """Check the style of commit message.

    :param: commit message
    :return: error messages if the checks fail
    """