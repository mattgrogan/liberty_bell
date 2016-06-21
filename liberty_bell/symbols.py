class Symbol(object):
    """ Superclass for symbols on the slot machine """

    def __init__(self):
        """ Initialize the symbol """

        self.name = ""
        self.value = 0

    def __str__(self):
        """ Convert to string """

        return self.name

    def __eq__(self, other):
        """ Check for equality """

        return self.value == other.value


class Liberty_Bell_Symbol(Symbol):
    """ Symbol to represent a Liberty Bell """

    def __init__(self):
        """ Initialize the symbol """

        self.name = "Liberty Bell"
        self.value = 1

class Heart_Symbol(Symbol):
    """ Symbol to represent a heart symbol """

    def __init__(self):
        """ Initialize the symbol """

        self.name = "Heart"
        self.value = 2

class Diamond_Symbol(Symbol):
    """ Symbol to represent a diamond """

    def __init__(self):
        """ Initialize the symbol """

        self.name = "Diamond"
        self.value = 3

class Spade_Symbol(Symbol):
    """ Symbol to represent a spade """

    def __init__(self):
        """ Initialize the symbol """

        self.name = "Spade"
        self.value = 4

class Horseshoe_Symbol(Symbol):
    """ Symbol to represent a Horseshoe """

    def __init__(self):
        """ Initialize the symbol """

        self.name = "Horseshoe"
        self.value = 5

class Star_Symbol(Symbol):
    """ Symbol to represent a star """

    def __init__(self):
        """ Initialize the symbol """

        self.name = "Star"
        self.value = 6

class Liberty_Bell_Symbols(object):
    """ An enumerator class to hold all the symbol references """

    def __init__(self):
        """ Initialize the symbols for this game """

        self.LIBERTY_BELL = Liberty_Bell_Symbol()
        self.HEART = Heart_Symbol()
        self.DIAMOND = Diamond_Symbol()
        self.SPADE = Spade_Symbol()
        self.HORSESHOE = Horseshoe_Symbol()
        self.STAR = Star_Symbol()
