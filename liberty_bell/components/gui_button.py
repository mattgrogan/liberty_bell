import Tkinter as tk


class GUI_Button(tk.Button, object):

  def __init__(self, name, *args, **kwargs):

    tk.Button.__init__(self, *args, width=10, height=1, **kwargs)

    self.name = name
    self._is_enabled = False

  @property
  def enabled(self):
    return self._is_enabled

  @enabled.setter
  def enabled(self, value):
    if value:
      self.configure(state=tk.NORMAL)
    else:
      self.configure(state=tk.DISABLED)
