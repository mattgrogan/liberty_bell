class Main_Controller(object):
  """ This is the main controller for the game. """

  def __init__(self):

    self.current_index = 0
    self.menu_items = []

  @property
  def current_item(self):
    """ Return the current item """

    if len(self.menu_items) == 0:
      raise ValueError("You must add menu items to the controller")

    return self.menu_items[self.current_index]

  def add_menu_item(self, menu_item):
    self.menu_items.append(menu_item)

  def move(self, step=1):

    self.current_index += step

    if self.current_index >= len(self.menu_items):
      self.current_index = 0
    elif self.current_index < 0:
      self.current_index = len(self.menu_items) - 1

  def handle_spin(self, message=None):
    self.current_item.handle_input("SPIN")

  def handle_up(self, message=None):
    self.current_item.handle_input("UP")

  def handle_down(self, message=None):
    self.current_item.handle_input("DOWN")

  def handle_b1(self, message=None):
    self.current_item.handle_input("B1")

  def handle_b2(self, message=None):
    self.current_item.handle_input("B2")

  def handle_b3(self, message=None):
    self.current_item.handle_input("B3")

  def handle_menu(self, message=None):
    self.current_item.handle_input("MENU")

  def run(self):
    return self.current_item.update()
