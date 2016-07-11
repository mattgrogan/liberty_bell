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
