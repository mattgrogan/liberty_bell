

class Slot_UI(object):
  """ UI for the slot machine """

  def __init__(self, *args, **kwargs):
    """ Initialize the UI """

    # Set up events
    events = ["spin_pressed", "up_pressed", "down_pressed",
              "menu_pressed", "b1_pressed", "b2_pressed", "b3_pressed"]
    self.events = {event: dict() for event in events}

    self._numeric_displays = {}

  def notify(self, event, message=None):
    """ Notify the subscribers for a particular event """

    for subscriber, callback in self.events[event].iteritems():
      callback(message)

  def register(self, event, who, callback=None):
    """ Register for updates """

    if callback is None:
      callback = getattr(who, 'update')

    self.events[event][who] = callback
