"""Test CommitCanvas using this file."""
import commitcanvas


class subject_capital_letter:
    """Check that subject line starts with capital letter."""

    @commitcanvas.check
    def rule(self, message: str):
        """Check that first character starts with lower case."""
        lines = message.splitlines()[0]
        if lines[0].islower():
            return "Subject must start with capital letter"


class subject_endwith_period:
    """Subject line of commit message ends with period."""

    @commitcanvas.check
    def rule(self, message: str):
        """Check last characte of first line."""
        lines = message.splitlines()
        if lines[0].endswith("."):
            return "Subject line can NOT end with period"
