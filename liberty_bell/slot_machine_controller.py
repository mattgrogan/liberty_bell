import time
import copy

import pygame
from pygame.locals import *

#from liberty_bell.ui.pygame_ui import Reel

view_size = (128, 300)

reel1_loc = (100, 100)
reel2_loc = (258, 100)
reel3_loc = (416, 100)

background_color = Color('white')

class PayoutAnimation(object):
    """ Tick up the amounts paid """

    def __init__(self, ui, controller, credits_from, credits_to):

        self.ui = ui
        self.controller = controller
        self.credits_from = credits_from
        self.credits_to = credits_to

    def execute(self):
        for i, credits in enumerate(range(self.credits_from + 1, self.credits_to + 1)):
            self.ui.credits_led.display(credits)
            self.ui.winner_paid_led.display(i + 1)
            self.ui.buzzer.increment_tone()
            time.sleep(0.10)


class SpinningState(object):

    def __init__(self, slot_machine, ui):

        self.slot_machine = slot_machine
        self.ui = ui
        #
        # self.r1 = Reel(self.slot_machine.reels[0].get_image(), self.ui.screen, reel1_loc, view_size)
        # self.r2 = Reel(self.slot_machine.reels[1].get_image(), self.ui.screen, reel2_loc, view_size)
        # self.r3 = Reel(self.slot_machine.reels[2].get_image(), self.ui.screen, reel3_loc, view_size)
        #
        # self.r1.blit()
        # self.r2.blit()
        # self.r3.blit()

        # Add the reels
        self.r1 = self.ui.screen.add_reel(self.slot_machine.reels[0].get_image(), reel1_loc, view_size)
        self.r2 = self.ui.screen.add_reel(self.slot_machine.reels[1].get_image(), reel2_loc, view_size)
        self.r3 = self.ui.screen.add_reel(self.slot_machine.reels[2].get_image(), reel3_loc, view_size)

        pygame.display.flip()

        self.ui.buzzer.button_tone()

        self.slot_machine.spin()

        import random
        self.r1.spin(3, self.slot_machine.reels[0].winning_stop)
        self.r2.spin(4, self.slot_machine.reels[1].winning_stop)
        self.r3.spin(5, self.slot_machine.reels[2].winning_stop)


        print "end init"

    def update(self):
        """ Animate the reels.

        self.active indicates if any reels are spinning

        """

        self.ui.menu_button.enabled = not self.r1.is_spinning

        self.ui.spin_button.enabled = self.slot_machine.can_spin
        self.ui.up_button.enabled = self.slot_machine.can_increase_bet
        self.ui.down_button.enabled = self.slot_machine.can_decrease_bet

        self.ui.reel1_button.enabled = False
        self.ui.reel2_button.enabled = False
        self.ui.reel3_button.enabled = False

        dirty_rects = []

        dirty_rects.append(self.r1.update())
        dirty_rects.append(self.r2.update())
        dirty_rects.append(self.r3.update())
        pygame.display.update(dirty_rects)

        if self.r1.is_spinning or self.r2.is_spinning or self.r3.is_spinning:
            next_state = self
        else:
            print "finished spinning"

            winner = self.slot_machine.eval_spin()

            if winner:
                start = self.slot_machine.prev_credits
                end = self.slot_machine.credits

                payout_anim = PayoutAnimation(self.ui, self, start, end)
                payout_anim.execute()

            next_state = ReadyState(self.slot_machine, self.ui)


        return next_state

    def handle_input(self):
        return self

class ReadyState(object):

    def __init__(self, slot_machine, ui):
        self.slot_machine = slot_machine
        self.ui = ui

    def update(self):
        self.ui.menu_button.enabled = not self.slot_machine.is_spinning

        self.ui.spin_button.enabled = self.slot_machine.can_spin
        self.ui.up_button.enabled = self.slot_machine.can_increase_bet
        self.ui.down_button.enabled = self.slot_machine.can_decrease_bet

        self.ui.reel1_button.enabled = False
        self.ui.reel2_button.enabled = False
        self.ui.reel3_button.enabled = False

        return self

    def handle_input(self, command):

        if command == "SPIN" and self.slot_machine.can_spin:
            print "Spinning..."
            next_state = SpinningState(self.slot_machine, self.ui)

        else:
            next_state = self

        return next_state

        # TODO: Handle UP and DOWN events

class Slot_Machine_Controller(object):

    def __init__(self, slot_machine, ui):

        self.ui = ui
        self.slot_machine = slot_machine
        self.options = {}
        self.options["AUTOPLAY"] = False

        self.state = ReadyState(self.slot_machine, self.ui)

    @property
    def name(self):
        return self.slot_machine.name

    def handle_input(self, command):

        self.state = self.state.handle_input(command)

        # if command == "UP":
        #     self.slot_machine.increment_bet()
        # if command == "DOWN":
        #     self.slot_machine.decrement_bet()
        # if command == "SPIN":
        #     if self.slot_machine.can_spin:
        #         self.enter_spin()
        #     else:
        #         self.options["AUTOPLAY"] = False

        self.update_button_state()
        self.update_display()

        return self

    def update_button_state(self):

        self.ui.menu_button.enabled = not self.slot_machine.is_spinning

        self.ui.spin_button.enabled = self.slot_machine.can_spin
        self.ui.up_button.enabled = self.slot_machine.can_increase_bet
        self.ui.down_button.enabled = self.slot_machine.can_decrease_bet

        self.ui.reel1_button.enabled = False
        self.ui.reel2_button.enabled = False
        self.ui.reel3_button.enabled = False

    def update_display(self):

        self.ui.credits_led.display(self.slot_machine.credits)
        self.ui.amount_bet_led.display(self.slot_machine.bet)

        if self.slot_machine.winner_paid > 0:
            self.ui.winner_paid_led.display(self.slot_machine.winner_paid)
        else:
            self.ui.winner_paid_led.clear()

    def start(self):
        self.update_button_state()
        self.update_display()

    def stop(self):

        for display in self.ui.reel_displays:
            display.clear()

        self.ui.amount_bet_led.clear()
        self.ui.winner_paid_led.clear()
        self.ui.credits_led.clear()

    def update(self):
        """ Update one iteration of game play """

        self.update_button_state()
        self.update_display()

        self.state = self.state.update()
