class Liberty_Bell_UI(object):

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
