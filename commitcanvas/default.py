import commitcanvas

class plug3:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        if message[0].islower():
            return("Commit must start with upparcase character") 


class plug1:
    @commitcanvas.hookimpl
    def rule(self,message:str):
        max_count = 100
        count = len(message)
        if count >= 100:
            return("Commit must have less than 100 characters, got: {}".format(count)) 