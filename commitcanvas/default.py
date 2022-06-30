"""Default rules for checking style of commit message."""
import commitcanvas


class subject_capital_letter:
    """Check that subject line starts with capital letter."""

    @commitcanvas.check
    def rule(self, message: str):
        """Check that first character starts with lower case."""
        lines = message.splitlines()[0]
        if lines[0].islower():
            return "Subject must start with capital letter"


class subject_max_char_count:
    """Check that subject line has less than 72 characters."""

    @commitcanvas.check
    def rule(self, message: str):
        """Compare number of characters with max count."""
        lines = message.splitlines()[0]
        max_count = 72
        count = len(lines)
        if count >= max_count:
            return "Subject line must have less \
                than {} characters, got: {}".format(
                max_count, count
            )


class subject_endwith_period:
    """Subject line of commit message ends with period."""

    @commitcanvas.check
    def rule(self, message: str):
        """Check last characte of first line."""
        lines = message.splitlines()
        if lines[0].endswith("."):
            return "Subject line can NOT end with period"


class blank_line:
    """There is blank line between subject and body."""

    @commitcanvas.check
    def rule(self, message: str):
        """Check that second line is empty in commit message."""
        lines = message.splitlines()
        if len(lines) > 1:
            if bool(lines[1]):
                return "Blank line between the subject and the body required"
