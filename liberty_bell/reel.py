import random


class Reel(object):
  """ A slot machine reel  """

  def __init__(self, index, stops, randomizer=random):
    """ Initialize the reel """

    self.index = index
    self.name = "Reel %i" % index
    self.stops = stops
    self.current_stop = 0
    self.current_spin = 0

    self.randomizer = randomizer

  def __str__(self):
    """ Print details """

    return str(self.name)

  def current_symbol(self):
    """ Return the current symbol to be shown in the ui """

    return self.stops[self.current_stop]

  def reset(self):
    """ Reset the current spin """

    self.current_spin = 0

  def advance(self):
    """ Advance the reel to the next stop and return the symbol """

    self.current_stop = self.current_stop + 1

    if self.current_stop >= len(self.stops):
      self.current_stop = 0  # go around
      self.current_spin = self.current_spin + 1

    return self.stops[self.current_stop]

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

    self.slot_reel = slot_reel
    self.winning_symbol = winning_symbol
    self.required_spins = required_spins

    # Reset the counter on the slot reel
    self.slot_reel.reset()

    # Hold the current references
    self._current_symbol = self.slot_reel.advance()
    self._current_iter = self._current_symbol.__iter__()

  def __iter__(self):
    """ Return self as an iterator """
    return self

  def next(self):
    """ Iterate through the symbols """

    if not self._current_iter.has_next():
      # Check for winner and advance to next symbol if not
      reached_required_spins = self.slot_reel.current_spin >= self.required_spins
      reached_winning_symbol = self._current_symbol == self.winning_symbol

      if reached_required_spins and reached_winning_symbol:
        raise StopIteration()
      else:
        self._current_symbol = self.slot_reel.advance()
        self._current_iter = self._current_symbol.__iter__()

    row_data = self._current_iter.next()

    return row_data
