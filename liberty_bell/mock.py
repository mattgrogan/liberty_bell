class MockRandom(object):
    """ Mock random.choice for testing """

    def __init__(self, sequence=None):
        """ Initialize at place zero """

        self.index = 0
        self.sequence = sequence

    def choice(self, stops):
        """ Return the item deterministicaly """

        # If we weren't passed a sequence of values, then just use
        # the stops.
        if self.sequence is None:
            self.sequence = range(len(stops))

        # Reset index if it's out of range
        if self.index >= len(self.sequence):
            self.index = 0

        # Find the result in the current item
        stop_index = self.sequence[self.index]
        result = stops[stop_index]

        self.index = self.index + 1
        return result

class Mock_Observer(object):
    """ Mock for testing events """

    def __init__(self):
        """ Initialize the event """

        self.fired = False
        self.message = None

    def observe(self, message):
        """ Called by the subject """

        self.fired = True
        self.message = message
