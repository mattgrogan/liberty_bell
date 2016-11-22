class Option_Return(object):

  def __init__(self, name, ui):
    self.name = name
    self.parent = None
    self.ui = ui
    self.has_options = False

  def start(self):

    pass

  def stop(self):
    pass

  def handle_input(self, command):
    if command == "SPIN":
      return None

  def update(self):
    return 100
