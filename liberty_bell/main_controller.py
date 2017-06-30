from liberty_bell.ui.liberty_bell_ui import Liberty_Bell_UI

from liberty_bell.slot_machine_controller import Slot_Machine_Controller
from liberty_bell.slot_machines.gold_award_machine import Gold_Award_Machine
from liberty_bell.slot_machines.liberty_bell_machine import \
    Liberty_Bell_Machine

from liberty_bell.menu_controller import Liberty_Bell_Menu


class StatePlay(object):
    """ This state handles all playing games """

    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, command):
        """ Handle input from the UI """

        if command == "MENU":
            self.controller.enter_menu()
        else:
            self.controller._current_item.handle_input(command)


class StateMenu(object):

    def __init__(self, controller):
        self.controller = controller

    def handle_input(self, command):
        if command == "MENU":
            if self.controller.menu.at_root:
                self.controller.enter_play()
            else:
                self.controller.menu.navigate_to("PARENT")
        elif command == "SPIN":
            self.controller.menu.invoke()
        elif command == "DOWN":
            self.controller.menu.navigate_to("DOWN")
        elif command == "UP":
            self.controller.menu.navigate_to("UP")


class MainController(object):
    """ This is the main controller for the game. """

    def __init__(self, ui_type):

        self.ui = Liberty_Bell_UI(ui_type)
        self.menu = Liberty_Bell_Menu(self, self.ui)

        self.state_play = StatePlay(self)
        self.state_menu = StateMenu(self)
        self._current_state = None
        self._current_item = None

        self.add_games()

        self.ui.attach(self.handle_input)

        self.ui.set_callback(self.run)
        self.ui.ready()

    def enter_menu(self):
        self._current_state = self.state_menu
        self.menu.enter_menu()

    def enter_play(self, game=None):
        if game is not None:
            self._current_item = game

        self._current_state = self.state_play
        self._current_item.start()

    def add_games(self):

        liberty_bell = Slot_Machine_Controller(Liberty_Bell_Machine(), self.ui)
        gold_award = Slot_Machine_Controller(Gold_Award_Machine(), self.ui)

        self.menu.add_game(liberty_bell.slot_machine.name, liberty_bell)
        self.menu.add_game(gold_award.slot_machine.name, gold_award)

        # Default to liberty bell
        self.menu.build_opts_menu(liberty_bell)
        self.enter_play(liberty_bell)

    def handle_input(self, command):

        self._current_state.handle_input(command)

    def run(self):
        if self._current_state == self.state_play:
            requested_delay_ms = self._current_item.update()
        else:
            requested_delay_ms = 10

        self.ui.concrete_ui.schedule_next(requested_delay_ms)

    def start(self):
        # TODO: Remove references to concrete_ui
        self.ui.concrete_ui.mainloop()

    def shutdown(self):
        self.ui.concrete_ui.shutdown()
