from screen import Liberty_Bell_Screen

class Liberty_Bell_UI(object):

    def __init__(self, concrete_ui_type):

        concrete_ui = self.get_concrete_ui(concrete_ui_type)

        concrete_ui.initialize(callback=self.notify)

        self.concrete_ui = concrete_ui

        self.screen = Liberty_Bell_Screen()

        self.spin_button = concrete_ui.spin_button
        self.up_button = concrete_ui.up_button
        self.down_button = concrete_ui.down_button
        self.menu_button = concrete_ui.menu_button

        self.reel1_button = concrete_ui.reel1_button
        self.reel2_button = concrete_ui.reel2_button
        self.reel3_button = concrete_ui.reel3_button

        self.credits_led = concrete_ui.credits_led
        self.winner_paid_led = concrete_ui.winner_paid_led
        self.amount_bet_led = concrete_ui.amount_bet_led

        self.buzzer = concrete_ui.buzzer

        self._observers = []

    def get_concrete_ui(self, concrete_ui_type):

        if concrete_ui_type == "rpi":
            from liberty_bell.ui.rpi import Rpi_UI
            ui = Rpi_UI()
        elif concrete_ui_type == "gui":
            from liberty_bell.ui.gui import Gui
            ui = Gui()
        else:
            raise ValueError("Unknown UI Type: %s" % concrete_ui_type)

        return ui

    def attach(self, observer):
        print "attaching"
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, event):
        print "notifing for %s" % event
        for observer in self._observers:
            observer(event)

    def ready(self):
        # This is a hack and needs to be removed
        self.concrete_ui.ready()

    def update(self):
        self.concrete_ui.update()
        #self.screen.update()
