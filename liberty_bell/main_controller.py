

class Main_Controller(object):
  """ This is the main controller for the game. """

  def __init__(self):

    self._current_index = 0
    self._current_item = None
    self.menu_items = []

  @property
  def current_item(self):

    if len(self.menu_items) == 0:
      raise ValueError("You must add menu items to the controller")
    elif self._current_item is None:
      self._current_item = self.menu_items[self._current_index]

    return self._current_item

  @current_item.setter
  def current_item(self, item):
    self._current_item = item

  def add_menu_item(self, menu_item):
    self.menu_items.append(menu_item)

  def move(self, step=1):

    self.current_item.stop()

    self._current_index += step

    if self._current_index >= len(self.menu_items):
      self._current_index = 0
    elif self._current_index < 0:
      self._current_index = len(self.menu_items) - 1

    self._current_item = self.menu_items[self._current_index]

    self.current_item.start()

  def handle_input(self, command):

    next_item = self.current_item.handle_input(command)

    if next_item is None:
      self.move()

    if next_item != self.current_item:
      self.current_item.stop()
      self.current_item = next_item
      self.current_item.start()

  def handle_spin(self, message=None):
    self.handle_input("SPIN")

  def handle_up(self, message=None):
    self.handle_input("UP")

  def handle_down(self, message=None):
    self.handle_input("DOWN")

  def handle_b1(self, message=None):
    self.handle_input("B1")

  def handle_b2(self, message=None):
    self.handle_input("B2")

  def handle_b3(self, message=None):
    self.handle_input("B3")

  def handle_menu(self, message=None):
    self.handle_input("MENU")

  def run(self):
    return self.current_item.update()
