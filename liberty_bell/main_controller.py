from functools import partial

from liberty_bell.text_menu.menu_engine import Menu_Engine
from liberty_bell.text_menu.menu_item import MenuItem


class Main_Controller(object):
  """ This is the main controller for the game. """

  def __init__(self):

    root_menu = MenuItem(
        "UPDATE_DISPLAY", "Press MENU to Return", self.execute_cmd)

    # Add credits
    buy_credits = MenuItem(
        "UPDATE_DISPLAY", "Buy Credits", self.execute_cmd)
    buy_1 = MenuItem("BUY_CREDITS", "Buy 1 Credit", self.execute_cmd, 1)
    buy_10 = MenuItem("BUY_CREDITS", "Buy 10 Credits", self.execute_cmd, 10)
    buy_100 = MenuItem("BUY_CREDITS", "Buy 100 Credits", self.execute_cmd, 100)
    buy_credits.add_child(buy_1)
    buy_credits.add_child(buy_10)
    buy_credits.add_child(buy_100)

    # Add various games
    game_menu = MenuItem("UPDATE_DISPLAY", "Select Game", self.switch_game)

    # Add options
    options = MenuItem("UPDATE_DISPLAY", "Options", self.execute_cmd)
    autoplay = MenuItem("TOGGLE_AUTOPLAY", "Toggle Autoplay", self.execute_cmd)
    options.add_child(autoplay)

    root_menu.add_child(buy_credits)
    root_menu.add_child(game_menu)
    root_menu.add_child(options)

    self.root_menu = root_menu
    self.game_menu = game_menu

    self._menu = Menu_Engine(buy_credits)
    self.menu_default = buy_credits
    self._current_state = "STATE_NONE"
    self.ui = None  # This is set later, needs a nice refactoring

  def execute_cmd(self, command_name, action, label, params=None):
    """ Obtain a command from the current item and execute it """

    print "Calling %s action %s label %s params %s" % (command_name, action, label, params)

    cmd = self._current_item.get_command(command_name, label, params)
    cmd.execute(action)

    if action == "ACTION_TRIGGER":
      self._menu.navigate_to("PARENT")

  def add_games(self, games):
    self._games = games
    self._current_item = self._games[0]
    self._current_state = "STATE_PLAY"

    # Create the game menu items
    top_game = MenuItem("SWITCH_GAME", games[
                        0].slot_machine.name, self.switch_game, games[0])

    self.game_menu.add_child(top_game)

    for i in range(len(games)):
      top_game.add_next(
          MenuItem("SWITCH_GAME", games[i].slot_machine.name, self.switch_game, games[i]))

  def switch_game(self, command_name, action, label, params=None):

    if action == "ACTION_LABEL":
      message = label
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()
    if action == "ACTION_DISPLAY":
      message = label + "\nPress SPIN"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()
    if action == "ACTION_TRIGGER":
      self._current_item = params
      self._menu.navigate(self.root_menu)
      self.current_state = "STATE_PLAY"

  def handle_input(self, command):
    print command
    print self._current_state

    if self._current_state == "STATE_PLAY":
      if command == "MENU":
        print "Entering menu"
        self._current_state = "STATE_MENU"
        self.enable_buttons()
        self._menu.navigate(self.menu_default)
      else:
        print "we should be playing now"
        # otherwise, we're in state play

        next_item = self._current_item.handle_input(command)

        if next_item != self._current_item:
          self._current_item.stop()
          self._current_item = next_item
          self._current_item.start()
    elif self._current_state == "STATE_MENU":
      if command == "MENU":
        if self._menu.current_item == self.root_menu:
          print "lets play"
          self._current_state = "STATE_PLAY"
        else:
          self._menu.navigate_to("PARENT")
      elif command == "SPIN":
        self._menu.invoke()
      elif command == "DOWN":
        self._menu.navigate_to("DOWN")
      elif command == "UP":
        self._menu.navigate_to("UP")

  def enable_buttons(self):
    self.ui.menu_button.enabled = True
    self.ui.spin_button.enabled = True
    self.ui.up_button.enabled = True
    self.ui.down_button.enabled = True

    self.ui.reel1_button.enabled = False
    self.ui.reel2_button.enabled = False
    self.ui.reel3_button.enabled = False

  def run(self):
    if self._current_state == "STATE_PLAY":
      requested_delay_ms = self._current_item.update()
    else:
      requested_delay_ms = 10

    self.ui.concrete_ui.schedule_next(requested_delay_ms)
