import Tkinter as tk


class Gui(tk.Tk):

  def __init__(self, controller):

    tk.Tk.__init__(self, None, None)

    self.controller = controller

    frame = tk.Frame(self)
    frame.grid(row=0, column=0, sticky=tk.W)

    self.after(0, self.start)

  def start(self):

    requested_delay_ms = self.controller.run()
    self.after(requested_delay_ms, self.start)
