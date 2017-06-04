from functools import partial

from liberty_bell.text_menu.menu_item import MenuItem

from liberty_bell.ui.liberty_bell_ui import Liberty_Bell_UI

from liberty_bell.slot_machine_controller import Slot_Machine_Controller
from liberty_bell.slot_machines.gold_award_machine import Gold_Award_Machine
from liberty_bell.slot_machines.liberty_bell_machine import \
    Liberty_Bell_Machine

from liberty_bell.menu_controller import Liberty_Bell_Menu


class State_Play(object):
    """ This state handles all playing games """

    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, command):
        """ Handle input from the UI """

        if command == "MENU":
            self.controller.enter_menu()
            # Pass the menu command onwards
            # self.controller.handle_input("MENU")
        else:
            self.controller._current_item.handle_input(command)


class State_Menu(object):

    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, command):
        if command == "MENU":
            if self.controller._menu.current_item == self.controller.root_menu:
                self.controller.enter_play()
            else:
                self.controller._menu.navigate_to("PARENT")
        elif command == "SPIN":
            self.controller._menu.invoke()
        elif command == "DOWN":
            self.controller._menu.navigate_to("DOWN")
        elif command == "UP":
            self.controller._menu.navigate_to("UP")


class Main_Controller(object):
    """ This is the main controller for the game. """

    def __init__(self, ui_type):

        self.ui = Liberty_Bell_UI(ui_type)
        self.menu = Liberty_Bell_Menu(self)

        self.root_menu = self.menu.root_menu
        self.game_menu = self.menu.game_menu

        self._menu = self.menu.menu

        self.state_play = State_Play(self)
        self.state_menu = State_Menu(self)
        self._current_state = None

        self.add_games()

        self.ui.attach(self.handle_input)

        self.ui.set_callback(self.run)
        self.ui.ready()

    def enter_menu(self):
        self._current_state = self.state_menu
        self.enable_buttons()
        self.menu.enter_menu()

    def enter_play(self):
        self._current_state = self.state_play

    def execute_cmd(self, command_name, action, label, params=None):
        """ Obtain a command from the current item and execute it """

        print "Calling %s action %s label %s params %s" % (command_name, action, label, params)

        cmd = self._current_item.get_command(command_name, label, params)
        cmd.execute(action)

        if action == "ACTION_TRIGGER":
            self._menu.navigate_to("PARENT")

    def add_games(self):

        liberty_bell = Slot_Machine_Controller(Liberty_Bell_Machine(), self.ui)
        gold_award = Slot_Machine_Controller(Gold_Award_Machine(), self.ui)

        games = [liberty_bell, gold_award]
        self._games = games
        self._current_item = self._games[0]
        self.enter_play()

        for i in range(len(games)):
            self.menu.add_game(games[i].slot_machine.name, games[i])

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
            self.enter_play()

    def handle_input(self, command):

        self._current_state.handle_input(command)

    def enable_buttons(self):
        self.ui.menu_button.enabled = True
        self.ui.spin_button.enabled = True
        self.ui.up_button.enabled = True
        self.ui.down_button.enabled = True

        self.ui.reel1_button.enabled = False
        self.ui.reel2_button.enabled = False
        self.ui.reel3_button.enabled = False

    def run(self):
        if self._current_state == self.state_play:
            requested_delay_ms = self._current_item.update()
        else:
            requested_delay_ms = 10

        self.ui.concrete_ui.schedule_next(requested_delay_ms)

    def start(self):
        self.ui.concrete_ui.mainloop()

    def shutdown(self):
        self.ui.concrete_ui.shutdown()
