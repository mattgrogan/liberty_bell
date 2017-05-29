class Switch_Game_Cmd(object):

  def __init__(self, ui, label, game):
    self.ui = ui
    self.label = label
    self.game = game

  def execute(self, action):

    if action == "ACTION_LABEL":
      message = self.label
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()
    if action == "ACTION_DISPLAY":
      message = self.label + " Press SPIN"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()
    if action == "ACTION_TRIGGER":
      self._current_item = params
      self._menu.navigate(self.root_menu)
      self.enter_play()


class Menu_Controller(object):

  def __init__(self, ui, controller):

    self.ui = ui
    self.controller = controller

  def get_command(self, command_name, label, params=None):

    if command_name == "SWITCH_GAME":
      cmd = Switch_Game_Cmd(self.ui, self.controller, label, game=params)

    return cmd
