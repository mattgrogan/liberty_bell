class MenuItem(object):

    def __init__(self, command_name, label, callback, params=None):

        self.command_name = command_name
        self.label = label
        self.callback = callback
        self.params = params

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

    def clear_children(self):
        """ Remove references to any child menu """

        self.child_item = None

    def execute_callback_action(self, action):
        self.callback(self.command_name, action, self.label, self.params)


class MenuItemCmd(MenuItem):

    def __init__(self, command):
        self.command = command

        self.next_item = None
        self.prev_item = None
        self.parent_item = None
        self.child_item = None

    def execute_callback_action(self, action):
        print "MenuItemCmd::execute_callback_action"
        self.execute(action)

    def execute(self, action):
        self.command.execute(action)
