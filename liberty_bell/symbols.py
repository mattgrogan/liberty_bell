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
