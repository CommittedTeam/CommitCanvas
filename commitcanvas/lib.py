import commitcanvas


@commitcanvas.hookimpl
def checkm(message):
    min_count = 2
    count = len(message.split(" "))
    if count <= min_count:
        print(f"Commit must have more than 3 words, got: {count}") 


@commitcanvas.hookimpl
def checkl(message):
    max_count = 100
    count = len(message)
    if count >= 100:
        print(f"Commit must have more than 100 characters, got: {count}") 

