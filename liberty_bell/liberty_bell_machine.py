from symbols import Symbol

class Liberty_Bell_Symbols(object):
    """ An enumerator class to hold all the symbol references """

    def __init__(self):
        """ Initialize the symbols for this game """

        self.LIBERTY_BELL = Symbol(name="Liberty Bell")
        self.HEART = Symbol(name="Heart")
        self.DIAMOND = Symbol(name="Diamond")
        self.SPADE = Symbol(name="Spade")
        self.HORSESHOE = Symbol(name="Horseshoe")
        self.STAR = Symbol(name="Star")
