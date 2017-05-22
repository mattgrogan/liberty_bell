import Tkinter as tk
import PIL.ImageTk as ImageTk

class GUI_1306(tk.Label, object):
  """ This behaves like the SSD1306 Display Adapter """

  def __init__(self, *args, **kwargs):

    tk.Label.__init__(self, *args, **kwargs)

  def display(self, image):
    """ Write image to the screen """

    tkimage = ImageTk.PhotoImage(image)

    self.image = tkimage
    self.configure(image=tkimage)
    self.update()
