from liberty_bell.text_menu.menu_engine import Menu_Engine
from liberty_bell.text_menu.menu_item import MenuItem, MenuItemCmd

class Switch_Game_Cmd(object):

    def __init__(self, ui, controller, label, game=None):
        self.ui = ui
        self.controller = controller
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
            self.controller.menu.navigate(self.controller.root_menu)
            self.controller.enter_play(self.game)


class Liberty_Bell_Menu(object):

    def __init__(self, controller, ui):

        self.controller = controller
        self.ui = ui

        root_menu = MenuItem(
            "UPDATE_DISPLAY", "Press MENU to Return", self.controller.execute_cmd)

        # Add credits
        buy_credits = MenuItem(
            "UPDATE_DISPLAY", "Buy Credits", self.controller.execute_cmd)
        buy_1 = MenuItem("BUY_CREDITS", "Buy 1 Credit", self.controller.execute_cmd, 1)
        buy_10 = MenuItem("BUY_CREDITS", "Buy 10 Credits",
                          self.controller.execute_cmd, 10)
        buy_100 = MenuItem("BUY_CREDITS", "Buy 100 Credits",
                           self.controller.execute_cmd, 100)
        buy_credits.add_child(buy_1)
        buy_credits.add_child(buy_10)
        buy_credits.add_child(buy_100)

        # Add various games
        game_cmd = Switch_Game_Cmd(self.ui, self.controller, "Switch Game")
        game_menu = MenuItemCmd("SWITCH_GAME", "Select Game", game_cmd)

        # Add options
        options = MenuItem("UPDATE_DISPLAY", "Options", self.controller.execute_cmd)
        autoplay = MenuItem("TOGGLE_AUTOPLAY",
                            "Toggle Autoplay", self.controller.execute_cmd)
        options.add_child(autoplay)

        root_menu.add_child(buy_credits)
        root_menu.add_child(game_menu)
        root_menu.add_child(options)

        self.root_menu = root_menu
        self.game_menu = game_menu

        self.menu_default = buy_credits

        self.menu = Menu_Engine(self.menu_default)

    def navigate(self, to):
        self.menu.navigate(to)

    def enter_menu(self):


        self.menu.navigate(self.menu_default)
        self.enable_buttons()

    def enable_buttons(self):
        self.ui.menu_button.enabled = True
        self.ui.spin_button.enabled = True
        self.ui.up_button.enabled = True
        self.ui.down_button.enabled = True

        self.ui.reel1_button.enabled = False
        self.ui.reel2_button.enabled = False
        self.ui.reel3_button.enabled = False

    def add_game(self, name, game):

        game_cmd = Switch_Game_Cmd(self.ui, self.controller, name, game)
        game = MenuItemCmd("SWITCH_GAME", name, game_cmd, game)
        self.game_menu.add_child(game)

    def get_command(self, command_name, label, params=None):

        print "WARNING: IN GET COMMAND ********************"

        if command_name == "SWITCH_GAME":
            cmd = Switch_Game_Cmd(self.ui, self.controller, label, game=params)

        return cmd
