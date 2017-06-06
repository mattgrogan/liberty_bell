

class Menu_Engine(object):
    """ Class to handle menu functionality """

    def __init__(self, initial_item):
        self.current_item = initial_item
        self.prev_item = None
        self.last_invoked_item = None

    def navigate(self, target_item):
        """ Navigate to the target item """

        if target_item is not None:
            self.prev_item = self.current_item
            self.current_item = target_item
            self.execute_callback_action("ACTION_LABEL")

    def navigate_to(self, direction):
        """ Navigate UP, DOWN, PARENT, CHILD  """

        if direction == "PARENT":
            self.navigate(self.current_item.parent_item)
        elif direction == "CHILD":
            self.navigate(self.current_item.child_item)
        elif direction == "DOWN":
            self.navigate(self.current_item.next_item)
        elif direction == "UP":
            self.navigate(self.current_item.prev_item)

    def invoke(self):

        prevent_trigger = False

        if self.last_invoked_item != self.current_item:
            print "Invoking for display"
            self.last_invoked_item = self.current_item
            prevent_trigger = True
            self.execute_callback_action("ACTION_DISPLAY")

        # Navigate to child
        if self.current_item.child_item is not None:
            print "Moving to child item"
            self.navigate(self.current_item.child_item)
        else:
            if not prevent_trigger:
                self.execute_callback_action("ACTION_TRIGGER")
                self.navigate_to("PARENT")

    def execute_callback_action(self, action):
        self.current_item.execute_callback_action(action)

    def render(self):
        pass
