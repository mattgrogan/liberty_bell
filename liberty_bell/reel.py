class Reel(object):
  """ A slot machine reel """

  def __init__(self, name, stops):
    """ Initialize the reel """

    self.name = name
    self.stops = stops

  def __str__(self):
    """ Print details """

    return str(self.name)
