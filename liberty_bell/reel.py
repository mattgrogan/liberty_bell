import random


class Reel(object):
  """ A slot machine reel  """

  def __init__(self, index, stops, randomizer=random):
    """ Initialize the reel """

    self.index = index
    self.name = "Reel %i" % index
    self.stops = stops

    self.randomizer = randomizer

  def __str__(self):
    """ Print details """

    return str(self.name)

  def get_symbol(self, stop):
    """ Return the current symbol to be shown in the ui """

    return self.stops[stop]

  def spin(self):
    """ Spin the reel and return a random result """

    return self.randomizer.choice(self.stops)

  def get_scroller(self, winning_symbol, required_spins):
    """ Return a scroller """

    scroller = Slot_Reel_Scroller(self, winning_symbol, required_spins)
    return scroller


class Slot_Reel_Scroller(object):
  """ This iterator will loop through each row of the images """

  def __init__(self, slot_reel, winning_symbol, required_spins):
    """ Initalize the iterator """

    self.current_stop = 0
    self.current_spin = 0
    self.required_spins = 0

    self.slot_reel = slot_reel
    self.current_row = 0
    self.current_symbol = self.slot_reel.get_symbol(self.current_stop)
    self.winning_symbol = winning_symbol

    self.required_spins = required_spins

  def __iter__(self):
    """ Return self as an iterator """
    return self

  def reset(self, required_spins=0):
    """ Reset the number of spins """

    self.current_spin = 0
    self.required_spins = required_spins

  def has_next(self, winning_symbol):
    """ Advance the current stop to the next stop """

    # If we've gone around the right number of times
    # AND we have the winning symbol, return False
    if self.current_spin >= self.required_spins and self.slot_reel.stops[self.current_stop] == winning_symbol:
      # No more to go
      return False
    else:
      # Move to next stops
      self.current_stop = self.current_stop + 1

      # Reset if we've reached the end
      if self.current_stop >= len(self.slot_reel.stops):
        self.current_stop = 0
        self.current_spin += 1

      # Keep going
      return True

  def next(self):
    """ Return the next item in the iteration """

    self.current_row = self.current_row + 1

    if self.current_row >= self.current_symbol.height:
      # Reached the end of the current symbol
      if self.has_next(self.winning_symbol):
        self.current_symbol = self.slot_reel.get_symbol(self.current_stop)
        self.current_row = 0
      else:
        # No more symbols
        raise StopIteration()

    # Return the details for the current row
    return self.current_symbol.get_row(self.current_row)
