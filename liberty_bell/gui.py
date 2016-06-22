import Tkinter as tk


class Slot_GUI(tk.Tk):
    """ Prototype GUI for the slot machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the GUI """

        tk.Tk.__init__(self, *args, **kwargs)

        # Add the spin button
        self.button = tk.Button(self, text="SPIN", command=self.spin_pressed)
        self.button.pack(side=tk.RIGHT)

        # Set up events
        events = ["SPIN_BUTTON_PRESSED"]

        self.events = {event: dict() for event in events}

    def _get_subscribers(self, event):
        """ Get the subscribers for a particular event """

        return self.events[event]

    def register(self, event, who, callback=None):
        """ Register for updates """

        if callback is None:
            callback = getattr(who, 'update')

        self._get_subscribers(event)[who] = callback

    def spin_pressed(self):
        """ Raise a notification to respond to the spin button pressed event """

        message = None
        subscribers = self._get_subscribers("SPIN_BUTTON_PRESSED")

        for subscriber, callback in subscribers.iteritems():
            callback(message)
