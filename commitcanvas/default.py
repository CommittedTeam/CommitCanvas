import commitcanvas

class subject_capital_letter:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        if message[0].islower():
            return("Commit must start with capital letter") 


class subject_max_char_count:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        max_count = 100
        count = len(message)
        if count >= 100:
            return("Commit must have less than 100 characters, got: {}".format(count)) 