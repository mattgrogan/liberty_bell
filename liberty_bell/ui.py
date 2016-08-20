from events import Events


class Slot_UI(object):
  """ UI for the slot machine """

  def __init__(self, *args, **kwargs):
    """ Initialize the UI """

    # Set up events
    events = [Events.SPIN, Events.INCREMENT_BET, Events.DECREMENT_BET]
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

  def add_numeric_display(self, name, display):
    """ Add a numeric display """

    if name in self._numeric_displays:
      self._numeric_displays[name].append(display)
    else:
      self._numeric_displays[name] = [display]

  def clear_numeric_display(self, name):
    """ Clear a numeric display """

    for numeric_display in self._numeric_displays[name]:
      numeric_display.clear()

  def update_numeric_display(self, name, val):
    """ Update the display to val """

    for numeric_display in self._numeric_displays[name]:
      numeric_display.display(val)

  def test_numeric_display(self, name):
    """ Test all numeric displays for name """
    for numeric_display in self._numeric_displays[name]:
      numeric_display.test()
