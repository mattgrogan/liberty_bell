class MenuItem(object):

  def __init__(self, label, callback):

    self.label = label
    self.callback = callback

    self.next_item = None
    self.prev_item = None
    self.parent_item = None
    self.child_item = None

  def add_next(self, item):
    self.next_item = item
    item.prev_item = self
    item.parent_item = self.parent_item
    return item

  def add_child(self, item):
    self.child_item = item
    item.parent_item = self
    return item
