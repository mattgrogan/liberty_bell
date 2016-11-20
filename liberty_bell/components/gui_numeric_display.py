import Tkinter as tk


class GUI_Numeric_Display(tk.Label):

  def __init__(self, name, *args, **kwargs):

    tk.Label.__init__(self, *args, relief=tk.SUNKEN, width=12, **kwargs)

    self.name = name

  def clear(self):

    self.configure(text="")
    self.update()

  def display(self, val):

    self.configure(text=val)
    self.update()
