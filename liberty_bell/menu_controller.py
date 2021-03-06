from liberty_bell.text_menu.menu_engine import Menu_Engine
from liberty_bell.text_menu.menu_item import MenuItem, MenuItemCmd


class Switch_Game_Cmd(object):

    def __init__(self, ui, controller, menu, label, game=None):
        self.ui = ui
        self.controller = controller
        self.menu = menu
        self.label = label
        self.game = game

    def execute(self, action):

        if action == "ACTION_LABEL":
            message = self.label
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(message)
            #self.ui.menu_display.flush()
        if action == "ACTION_DISPLAY":
            message = self.label + " Press SPIN"
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(message)
            #self.ui.menu_display.flush()
        if action == "ACTION_TRIGGER":
            self.menu.build_opts_menu(self.game)
            self.controller.menu.navigate(self.controller.menu.root_menu)
            self.controller.enter_play(self.game)


class Liberty_Bell_Menu(object):

    def __init__(self, controller, ui):

        self.controller = controller
        self.ui = ui

        root_cmd = Update_Display_Cmd(self.ui, "Press Menu to Return")
        root_menu = MenuItemCmd(root_cmd)

        game_cmd = Switch_Game_Cmd(
            self.ui, self.controller, self, "Switch Game")
        game_menu = MenuItemCmd(game_cmd)

        options_cmd = Update_Display_Cmd(self.ui, "Game Options")
        opts_menu = MenuItemCmd(options_cmd)

        root_menu.add_child(game_menu)
        root_menu.add_child(opts_menu)

        self.root_menu = root_menu
        self.game_menu = game_menu
        self.opts_menu = opts_menu

        self.menu_default = game_menu

        self.menu = Menu_Engine(self.menu_default)

    def navigate(self, to):
        self.menu.navigate(to)

    def navigate_to(self, dir):
        self.menu.navigate_to(dir)

    def invoke(self):
        self.menu.invoke()

    @property
    def at_root(self):
        return self.menu.at_root

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

    def build_opts_menu(self, game):
        """ Set up the user options menu. Must be called after game is set. """

        self.opts_menu.clear_children()

        for opt in game.user_opts:
            cmd = MenuItemCmd(opt)
            self.opts_menu.add_child(cmd)

    def add_game(self, name, game):
        game_cmd = Switch_Game_Cmd(self.ui, self.controller, self, name, game)
        game_menu = MenuItemCmd(game_cmd)
        self.game_menu.add_child(game_menu)
