class Symbol(object):
    """ Superclass for symbols on the slot machine """

    def __init__(self, name):
        """ Initialize the symbol """

        self.name = name

    def __str__(self):
        """ Convert to string """

        return self.name

    def __eq__(self, other):
        """ Check for equality """

        return self.name == other.name

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
