from functools import partial

from liberty_bell.text_menu.menu_engine import Menu_Engine
from liberty_bell.text_menu.menu_item import MenuItem


class Main_Controller(object):
  """ This is the main controller for the game. """

  def __init__(self):

    root_menu = MenuItem("Press MENU to Return", self.handle_action)

    # Add credits
    buy_credits = MenuItem("Buy Credits...", self.handle_action)
    buy_1 = MenuItem("Buy 1 credit", partial(self.buy_credits, 1))
    buy_10 = MenuItem("Buy 10 credits", partial(self.buy_credits, 10))
    buy_100 = MenuItem("Buy 100 credits", partial(self.buy_credits, 100))
    buy_credits.add_child(buy_1)
    buy_credits.add_child(buy_10)
    buy_credits.add_child(buy_100)

    # Add various games
    game_menu = MenuItem("Select Game...", self.handle_action)

    # Add options
    options = MenuItem("Options...", self.handle_action)
    autoplay = MenuItem("Toggle Autoplay", self.toggle_autoplay)
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

  def toggle_autoplay(self, action, caller):
    print "Received action %s on %s" % (action, caller.label)
    message = "Autoplay: "

    autoplay = self._current_item.options["AUTOPLAY"]

    if action == "ACTION_LABEL":
      message += "ON" if autoplay else "OFF"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()

    if action == "ACTION_DISPLAY":
      message = "Press SPIN to Save"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_menu_text(message, headline="CONFIRM?")
      self.ui.menu_display.flush()

    if action == "ACTION_TRIGGER":
      self._current_item.options["AUTOPLAY"] = not autoplay
      self._menu.navigate_to("PARENT")

  def handle_action(self, action, caller):

    print "Received action %s on %s" % (action, caller.label)

    if action == "ACTION_LABEL":
      message = caller.label
      self.ui.menu_display.clear()
      self.ui.menu_display.add_menu_text(message)
      self.ui.menu_display.flush()

  def buy_credits(self, amount, action, caller):

    print "Received action %s from '%s' for %s" % (action, caller.label, amount)

    if action == "ACTION_LABEL":
      message = caller.label
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()

    if action == "ACTION_DISPLAY":
      message = caller.label + "\nPress SPIN"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()

    if action == "ACTION_TRIGGER":
      self._current_item.slot_machine.credits += amount
      self._current_item.update_display()
      self._menu.navigate_to("PARENT")

  def add_games(self, games):
    self._games = games
    self._current_item = self._games[0]
    self._current_state = "STATE_PLAY"

    # Create the game menu items
    top_game = MenuItem(games[0].slot_machine.name,
                        partial(self.switch_game, games[0]))

    self.game_menu.add_child(top_game)

    for i in range(len(games)):
      top_game.add_next(
          MenuItem(games[i].slot_machine.name, partial(self.switch_game, games[i])))

  def switch_game(self, game, action, caller):
    print "Received action %s from '%s' for %s" % (action, caller.label, game)

    if action == "ACTION_LABEL":
      message = caller.label
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()
    if action == "ACTION_DISPLAY":
      message = caller.label + "\nPress SPIN"
      self.ui.menu_display.clear()
      self.ui.menu_display.add_line(message)
      self.ui.menu_display.flush()
    if action == "ACTION_TRIGGER":
      self._current_item = game
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

    self.ui.schedule_next(requested_delay_ms)
