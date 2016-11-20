class Symbol(object):
  """ Superclass for symbols on the slot machine """

  def __init__(self, name, image=None):
    """ Initialize the symbol """

    self.name = name
    self.image = image

  def __str__(self):
    return self.name

  def __eq__(self, other):
    return self.name == other.name
