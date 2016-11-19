import copy
import random


class Reel(object):
  """ A slot machine reel  """

  def __init__(self, index, stops, randomizer=random):
    """ Initialize the reel """

    self.index = index
    self.name = "Reel %i" % (index + 1)
    self.stops = copy.deepcopy(stops)

    self.winning_symbol = None

    self.current_stop = 0
    self.current_spin = 0

    self.min_spins = index + 1

    self.randomizer = randomizer

  def __str__(self):
    return str(self.name)

  @property
  def current_symbol(self):
    """ Return the current symbol to be shown in the ui """

    return self.stops[self.current_stop]

  def advance(self):
    """ Advance the reel to the next stop and return the symbol """

    self.current_stop = self.current_stop + 1

    if self.current_stop >= len(self.stops):
      self.current_stop = 0  # go around
      self.current_spin = self.current_spin + 1

    self.current_symbol.reset()

  def spin(self):
    """ Spin the reel and return a random result """

    self.winning_symbol = self.randomizer.choice(self.stops)
    self.current_spin = 0

  def next_line(self):
    """ Get the next line from the symbol """

    try:
      line = self.current_symbol.next_line()
    except StopIteration:
      if self.current_symbol == self.winning_symbol and self.current_spin >= self.min_spins:
        raise StopIteration  # reached the end
      else:
        self.advance()
        line = self.current_symbol.next_line()

    return line
