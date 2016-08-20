from events import Events


class Slot_UI(object):
  """ UI for the slot machine """

  def __init__(self, *args, **kwargs):
    """ Initialize the UI """

    # Set up events
    events = [Events.SPIN, Events.INCREMENT_BET, Events.DECREMENT_BET]
    self.events = {event: dict() for event in events}
    self.buttons = {}

    self._numeric_displays = {}
    self._reel_displays = {}

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

  def add_reel_display(self, name, display):
    """ Add a reel display """

    if name in self._reel_displays:
      self._reel_displays[name].append(display)
    else:
      self._reel_displays[name] = [display]

  def clear_reel_display(self, name):
    """ Clear a reel display """

    for reel_display in self._reel_displays[name]:
      reel_display.clear()

  def update_reel_display(self, name, val):
    """ Update the display to val """

    for reel_display in self._reel_displays[name]:
      reel_display.display(val)

  def test_reel_display(self, name):
    """ Test all reel displays for name """
    for reel_display in self._reel_displays[name]:
      reel_display.test()

  def show_test_pattern(self, name):
    """ Display a test pattern """

    for reel_display in self._reel_displays[name]:
      reel_display.show_test_pattern()

  def add_button(self, button):
    """ Add a button to the UI """

    self.buttons[button.name] = button

  def enable_button(self, name):
    """ Enable the button """

    self.buttons[name].enable()

  def disable_button(self, name):
    """ Disable the button """

    self.buttons[name].disable()

  def button_pressed(self, name):
    """ Return true if the button was pressed """

    return self.buttons[name].event_detected
