class Cancel(Exception): pass

class Quit(Exception):
    def __str__(self):
        return ("quit...")