class Liberty_Bell_UI(object):

  def __init__(self, ui_factory):

    self.spin_button = ui_factory.spin_button()
    self.up_button = ui_factory.up_button()
    self.down_button = ui_factory.down_button()
    self.menu_button = ui_factory.menu_button()

    self.display_1 = ui_factory.display_1()
    self.display_2 = ui_factory.display_2()
    self.display_3 = ui_factory.display_3()

    self.menu_display = ui_factory.menu_display()

  def start_observer(self):
    self._observers = []

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
