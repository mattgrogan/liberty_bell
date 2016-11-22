from liberty_bell.menu import Menu


class Option_Controller(Menu):

  def __init__(self, parent, ui, *args, **kwargs):
    super(Option_Controller, self).__init__(*args, **kwargs)

    self.parent = parent
    self.ui = ui

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
    self.ui.menu_display.display()

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
