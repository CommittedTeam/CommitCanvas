"""Default rules for checking style of commit message"""
import commitcanvas

class subject_capital_letter:
    @commitcanvas.check
    def rule(self,message:str):
        """Subject line of commit message starts with capital letter."""
        if message[0].islower():
            return("Subject must start with capital letter") 


class subject_max_char_count:
    @commitcanvas.check
    def rule(self,message:str):
        """Number of characters in subject line of commit message does not exceed 72."""
        lines = message.splitlines()[0]
        max_count = 72
        count = len(lines)
        if count >= max_count:
            return("Subject line must have less than {} characters, got: {}".format(max_count,count)) 


class subject_endwith_period:
    @commitcanvas.check
    def rule(self,message:str):
        """Subject line of commit message ends with period."""
        lines = message.splitlines()
        if lines[0].endswith("."):
            return("Subject line can NOT end with period")


class blank_line:
    @commitcanvas.check
    def rule(self,message:str):
        """There is blank line between subject and body."""
        lines = message.splitlines()
        if len(lines) > 1:
            if bool(lines[1]):
               return("Commit message must have blank line between the subject and the body") 



