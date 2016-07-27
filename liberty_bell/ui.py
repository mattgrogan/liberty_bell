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
    self.buttons = {}

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

  def add_button(self, button):
    """ Add a button to the UI """

    self.buttons[button.name] = button

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

  def enable_button(self, name):
    """ Enable the button """

    self.buttons[name].enable()

  def disable_button(self, name):
    """ Disable the button """

    self.buttons[name].disable()

  def button_pressed(self, name):
    """ Return true if the button was pressed """

    return self.buttons[name].event_detected
