from liberty_bell.ui.liberty_bell_ui import Liberty_Bell_UI

from liberty_bell.slot_machine_controller import Slot_Machine_Controller
from liberty_bell.slot_machines.gold_award_machine import Gold_Award_Machine
from liberty_bell.slot_machines.liberty_bell_machine import \
    Liberty_Bell_Machine

#from liberty_bell.menu_controller import Liberty_Bell_Menu


import pygame
FPS = 60


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
        self.clock = pygame.time.Clock()
        self.game = Slot_Machine_Controller(Liberty_Bell_Machine(), self.ui)

        self.ui.attach(self.handle_input)

    def handle_input(self, command):

        self.game.handle_input(command)

    def start(self):

        done = False

        while not done:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        done = True
                        break
                elif event.type == pygame.QUIT:
                    done = True
                    break
            if done:
                break

            self.game.update()
            # Comment for rpi ui
            #self.ui.concrete_ui.update()
            pygame.display.update()

            self.clock.tick(FPS)

    def shutdown(self):
        self.ui.concrete_ui.shutdown()
