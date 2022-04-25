import commitcanvas

class subject_capital_letter:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        if message[0].islower():
            return("Subject must start with capital letter") 


class subject_max_char_count:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        lines = message.splitlines()[0]
        max_count = 72
        count = len(lines)
        if count >= max_count:
            return("Subject line must have less than {} characters, got: {}".format(max_count,count)) 


class subject_endwith_period:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        lines = message.splitlines()
        if lines[0].endswith("."):
            return("Subject line can NOT end with period")


class blank_line:
    @commitcanvas.hookimpl
    def rule(self,message:str):

        lines = message.splitlines()
        if len(lines) > 1:
            if not lines[1]:
               return("Commit message must have blank line between the subject and the body") 



