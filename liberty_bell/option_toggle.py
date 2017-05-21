class Option_Toggle(object):

  def __init__(self, name, ui, default):

    self.name = name
    self.parent = None
    self.ui = ui
    self.value = default
    self.has_options = True

  def start(self):

    self.ui.menu_button.enabled = True
    self.ui.spin_button.enabled = True
    self.ui.up_button.enabled = True
    self.ui.down_button.enabled = True

    self.ui.reel1_button.enabled = False
    self.ui.reel2_button.enabled = False
    self.ui.reel3_button.enabled = False

    self.update_display()

  def stop(self):
    self.ui.menu_display.clear()

  def update_display(self):
    message = "%s: %s" % (self.name, "On" if self.value else "Off")

    self.ui.menu_display.blank()
    self.ui.menu_display.text(message)
    self.ui.menu_display.display()

  def toggle(self):
    self.value = not self.value

  def handle_input(self, command):
    if command in ["UP", "DOWN"]:
      self.toggle()
      return self
    if command in ["MENU", "SPIN"]:
      return self.parent

  def update(self):
    self.update_display()
    return 100