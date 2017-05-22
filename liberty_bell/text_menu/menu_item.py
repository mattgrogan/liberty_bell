class MenuItem(object):

  def __init__(self, label, callback):

    self.label = label
    self.callback = callback

    self.next_item = None
    self.prev_item = None
    self.parent_item = None
    self.child_item = None

  def add_next(self, item):
    if self.next_item is None:
      self.next_item = item
      item.prev_item = self
      item.parent_item = self.parent_item
    else:
      self.next_item.add_next(item)

  def add_child(self, item):
    if self.child_item is None:
      self.child_item = item
      item.parent_item = self
    else:
      self.child_item.add_next(item)

  def label(self):
    self.command.label()

  def display(self):
    self.command.display()

  def trigger(self):
    self.command.trigger()
