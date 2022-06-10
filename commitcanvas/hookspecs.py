"""Define hook spec."""
import pluggy

hookspec = pluggy.HookspecMarker("commitcanvas")


@hookspec
def rule(message: str):
    """Check the style of commit message.

    :param: commit message
    :return: error messages if the check fails
    """
