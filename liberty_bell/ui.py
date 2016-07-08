from events import Events


class Slot_UI(object):
    """ UI for the slot machine.

    The controller will call when these items need to be updated:
    update_credits(), update_bet(), update_reel(), update_winner_paid()

    You must call these functions in the event of a ui event:
    on_increment_bet_press(), on_decrement_bet_press(), on_spin_press()

    We're also expecting a mainloop()
    """

    def __init__(self, *args, **kwargs):
        """ Initialize the UI """

        # Set up events
        events = [Events.SPIN, Events.INCREMENT_BET, Events.DECREMENT_BET]
        self.events = {event: dict() for event in events}

    def notify(self, event, message=None):
        """ Notify the subscribers for a particular event """

        for subscriber, callback in self.events[event].iteritems():
            callback(message)

    def register(self, event, who, callback=None):
        """ Register for updates """

        if callback is None:
            callback = getattr(who, 'update')

        self.events[event][who] = callback

    def on_spin_press(self):
        """ Raise a notification to respond to the spin button pressed event """

        self.notify(Events.SPIN)

    def on_increment_bet_press(self):
        """ Fire event for incrementing bet """

        self.notify(Events.INCREMENT_BET)

    def on_decrement_bet_press(self):
        """ Fire event for decrementing bet """

        self.notify(Events.DECREMENT_BET)

    def update_credits(self, credits):
        """ Update the credits box """

        raise(NotImplementedError)

    def update_bet(self, bet):
        """ Update the bet """

        raise(NotImplementedError)

    def update_winner_paid(self, winner_paid):
        """ Print the amount paid """

        raise(NotImplementedError)

    def update_reel(self, reel, symbol):
        """ Update reel with the result """

        raise(NotImplementedError)
