import time
import copy


class Buy_Credits_Cmd(object):

    def __init__(self, ui, slot_machine, controller, amount):
        self.ui = ui
        self.slot_machine = slot_machine
        self.controller = controller
        self.amount = amount

    def execute(self, action):

        if action == "ACTION_LABEL":
            message = "Buy %i credit(s)" % self.amount
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(message)
            #self.ui.menu_display.flush()

        if action == "ACTION_DISPLAY":
            message = "Buying %i Press SPIN" % self.amount
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(message)
            #self.ui.menu_display.flush()

        if action == "ACTION_TRIGGER":
            self.slot_machine.credits += self.amount
            self.controller.update_display()


class Toggle_Autoplay_Cmd(object):

    def __init__(self, ui, controller):
        self.ui = ui
        self.controller = controller

    def execute(self, action):
        message = "Autoplay: "

        autoplay = self.controller.options["AUTOPLAY"]

        print "Autoplay: %s" % action

        if action == "ACTION_LABEL":
            message += "ON" if autoplay else "OFF"
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(message)
            #self.ui.menu_display.flush()

        if action == "ACTION_DISPLAY":
            message += "ON" if not autoplay else "OFF"
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(message, headline="CONFIRM?")
            #self.ui.menu_display.flush()

        if action == "ACTION_TRIGGER":
            # self.controller.menu.navigate(self.controller.root_menu)
            print "Triggering autoplay to %s" % (not autoplay)
            self.controller.options["AUTOPLAY"] = not autoplay
            self.controller.enter_ready()

# TODO: Move this to UI


class Update_Display_Cmd(object):

    def __init__(self, ui, text):
        self.ui = ui
        self.text = text

    def execute(self, action):
        print "Received action %s from '%s'" % (action, self.text)

        if action == "ACTION_LABEL":
            #self.ui.menu_display.clear()
            #self.ui.menu_display.add_menu_text(self.text)
            #self.ui.menu_display.flush()
            pass


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
            self.controller.update_menu_display(credits=credits)
            self.ui.buzzer.increment_tone()
            time.sleep(0.10)


class SpinningState(object):

    def __init__(self, ui, controller, slot_machine):
        self.ui = ui
        self.controller = controller
        self.slot_machine = slot_machine

        self.active = False

    def update(self):
        """ Animate the reels.

        self.active indicates if any reels are spinning

        """

        requested_delay_ms = 0

        self.active = False

        for i, reel in enumerate(self.slot_machine.reels):
            try:
                line = reel.next_line()
                self.active = True
                self.ui.reel_displays[i].write_line(line)
            except StopIteration:
                pass

        if not self.active:
            self.controller.eval()

        return requested_delay_ms


class ReadyState(object):

    def __init__(self):
        pass

    def update(self):
        return 100  # Return the requested delay


class AutoplayState(object):

    def __init__(self, ui, controller):
        self.ui = ui
        self.controller = controller
        self.ticks = 0
        self.max_ticks = 5

    def update(self):

        requested_delay_ms = 1000

        msg = "Autoplay in %s" % (self.max_ticks - self.ticks)

        #self.ui.menu_display.add_line_nbr(msg, 2)
        #self.ui.menu_display.flush()

        self.ticks += 1

        if self.ticks > self.max_ticks:
            self.controller.enter_spin()

        return requested_delay_ms


class Slot_Machine_Controller(object):

    def __init__(self, slot_machine, ui):

        self.ui = ui
        self.slot_machine = slot_machine
        self.options = {}
        self.options["AUTOPLAY"] = False

        self.user_opts = []

        # Options for purchasing credits
        self.user_opts.append(Buy_Credits_Cmd(
            self.ui, self.slot_machine, self, 1))
        self.user_opts.append(Buy_Credits_Cmd(
            self.ui, self.slot_machine, self, 10))
        self.user_opts.append(Buy_Credits_Cmd(
            self.ui, self.slot_machine, self, 100))

        self.user_opts.append(Toggle_Autoplay_Cmd(self.ui, self))

        self.enter_ready()

    @property
    def name(self):
        return self.slot_machine.name

    def handle_input(self, command):

        if command == "UP":
            self.slot_machine.increment_bet()
        if command == "DOWN":
            self.slot_machine.decrement_bet()
        if command == "SPIN":
            if self.slot_machine.can_spin:
                self.enter_spin()
            else:
                self.options["AUTOPLAY"] = False

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

    def update_menu_display(self, credits=None):
        """ Update the credit and cash amounts on the menu display """

        if credits is None:
            credits = self.slot_machine.credits

        line1 = "1 CR = $%0.2f" % self.slot_machine.denomination
        line2 = "Cash: $%.2f" % (self.slot_machine.denomination * credits)
        line3 = "  GOOD LUCK"

        #self.ui.menu_display.clear()
        #self.ui.menu_display.add_line_nbr(line1, 0)
        #self.ui.menu_display.add_line_nbr(line2, 1)

        #if self.slot_machine.is_spinning:
            #self.ui.menu_display.add_line_nbr(line3, 3, inverse=True)

        #self.ui.menu_display.flush()

    def update_display(self):

        self.update_menu_display()

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

    def enter_spin(self):
        """ Enter the spinning state """

        self.ui.buzzer.button_tone()
        self.slot_machine.spin()

        # These have to happen after spin!
        self.update_button_state()
        self.update_display()

        self.state = SpinningState(self.ui, self, self.slot_machine)

    def eval(self):
        """ Evaluate the spin"""

        winner = self.slot_machine.eval_spin()

        if winner:
            # Do a nice animation =)
            start = self.slot_machine.prev_credits
            end = self.slot_machine.credits

            payout_anim = PayoutAnimation(self.ui, self, start, end)
            payout_anim.execute()

        else:
            self.ui.buzzer.lose_tone()

        self.enter_ready()

    def enter_ready(self):
        """ Enter the ready for spin state """

        print "In enter_ready() for %s" % self.slot_machine.name
        self.update_button_state()
        self.update_display()
        self.state = ReadyState()

        if self.options["AUTOPLAY"]:
            self.state = AutoplayState(self.ui, self)

    def update(self):
        """ Update one iteration of game play """

        requested_delay_ms = self.state.update()

        return requested_delay_ms
