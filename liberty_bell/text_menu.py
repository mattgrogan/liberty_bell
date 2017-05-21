class Menu(object):
  """ Superclass for holding the menu interface """

  def __init__(self, *args, **kwargs):

    #super(Menu, self).__init__(*args, **kwargs)
    self._index = 0
    self._selected = None
    self._items = []
    self._items_dict = {}

  @property
  def current_item(self):

    if len(self._items) == 0:
      raise ValueError("No items in the menu")
    elif self._selected is None:
      self._selected = self._items[self._index]

    return self._selected

  @current_item.setter
  def current_item(self, item):
    """ This lets you set an item that is not in the items list """
    self._selected = item

  def __getitem__(self, key):
    return self._items_dict[key]

  def append(self, item):
    self._items.append(item)
    self._items_dict[item.name] = item

  def move(self, step=1):

    self._index += step

    if self._index >= len(self._items):
      self._index = 0
    elif self._index < 0:
      self._index = len(self._items) - 1

    self.current_item = self._items[self._index]
