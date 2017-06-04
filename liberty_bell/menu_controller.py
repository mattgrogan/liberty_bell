from liberty_bell.text_menu.menu_engine import Menu_Engine
from liberty_bell.text_menu.menu_item import MenuItem

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


class Liberty_Bell_Menu(object):

    def __init__(self, controller):

        self.controller = controller

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
        game_menu = MenuItem("UPDATE_DISPLAY", "Select Game", self.controller.switch_game)

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




    def enter_menu(self):


        self.menu.navigate(self.menu_default)

    def get_command(self, command_name, label, params=None):

        if command_name == "SWITCH_GAME":
            cmd = Switch_Game_Cmd(self.ui, self.controller, label, game=params)

        return cmd
