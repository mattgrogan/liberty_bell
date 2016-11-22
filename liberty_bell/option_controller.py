

class Option_Controller(object):

  def __init__(self, parent, ui):

    self.parent = parent
    self.ui = ui

    self._options = []
    self._options_dict = {}

    self._current_index = 0

  @property
  def current_item(self):

    if len(self._options) == 0:
      raise ValueError("You must add menu items to the controller")
    else:
      return self._options[self._current_index]

  def move(self, step=1):

    self._current_index += step

    if self._current_index >= len(self._options):
      self._current_index = 0
    elif self._current_index < 0:
      self._current_index = len(self._options) - 1

  def append(self, option):
    option.parent = self
    self._options.append(option)
    self._options_dict[option.name] = option

  def __getitem__(self, key):
    return self._options_dict[key]

  def start(self):

    self.ui.menu_button.enabled = True
    self.ui.spin_button.enabled = True
    self.ui.up_button.enabled = True
    self.ui.down_button.enabled = True

    self.ui.reel1_button.enabled = False
    self.ui.reel2_button.enabled = False
    self.ui.reel3_button.enabled = False

    self.update_display()

  def update_display(self):
    message = "Game Options: %s" % self.current_item.name
    self.ui.menu_display.blank()
    self.ui.menu_display.text(message)
    self.ui.menu_display.update()

  def stop(self):
    self.ui.menu_display.clear()

  def handle_input(self, command):
    if command == "DOWN":
      self.move(1)
    if command == "UP":
      self.move(-1)
    if command == "SPIN":
      # Check if this item has other options
      # TODO: Handle this with overloading
      if self.current_item.has_options:
        return self.current_item
      else:
        return self.current_item.handle_input("SPIN")

    if command == "MENU":
      return self.parent

    return self

  def update(self):
    self.update_display()
    return 100
    # return self.current_item.update()
