import random

class Reel(object):
    """ A slot machine reel  """

    def __init__(self, name, stops, randomizer=random):
        """ Initialize the reel """

        self.name = name
        self.stops = stops

        self.current_stop = 0
        self.current_spin = 0
        self.required_spins = 0

        self.randomizer = randomizer

    def __str__(self):
        """ Print details """

        return str(self.name)

    def reset(self, required_spins=0):
        """ Reset the number of spins """

        self.current_spin = 0
        self.required_spins = required_spins

    def has_next(self, winning_symbol):
        """ Advance the current stop to the next stop """

        # If we've gone around the right number of times
        # AND we have the winning symbol, return False
        if self.current_spin >= self.required_spins and self.stops[self.current_stop] == winning_symbol:
            # No more to go
            return False
        else:
            # Move to next stops
            self.current_stop = self.current_stop + 1

            # Reset if we've reached the end
            if self.current_stop >= len(self.stops):
                self.current_stop = 0
                self.current_spin += 1

            # Keep going
            return True

    def get_current_symbol(self):
        """ Return the current symbol to be shown in the ui """

        return self.stops[self.current_stop]

    def spin(self):
        """ Spin the reel and return a random result """

        return self.randomizer.choice(self.stops)

class Slot_Reel_Scroller(object):
    """ This iterator will loop through each line of the images """

    def __init__(self, slot_reel, nbr_symbols, max_rows):
        """ Initalize the iterator """

        self.slot_reel = slot_reel
        self.nbr_symbols = nbr_symbols
        self.max_rows = max_rows

        self.current_symbol = 0
        self.current_row = 0

    def __iter__(self):
        """ Return self as an iterator """
        return self

    def next(self):
        """ Return the next item in the iteration """

        self.current_row = self.current_row + 1
                
        if self.current_row >= self.max_rows:
            # Reached the end of the current symbol
            self.current_symbol = self.current_symbol + 1
            self.current_row = 0

        if self.current_symbol >= self.nbr_symbols:
            self.current_symbol = 0

        # Return the details for the current row
        return self.slot_reel.get_row(self.current_symbol, self.current_row)
