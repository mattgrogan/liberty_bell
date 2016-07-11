import random
import time
import Tkinter as tk

from PIL import ImageTk

from events import Events
from ui import Slot_UI


class Slot_GUI(Slot_UI, tk.Tk):
  """ Prototype GUI for the slot machine """

  def __init__(self, reels=None, **kwargs):
    """ Initialize the GUI """

    super(Slot_GUI, self).__init__(None, **kwargs)
    tk.Tk.__init__(self, None, **kwargs)

    self.reels = reels
    self.current_stops = [0] * len(self.reels)

    # Add the buttons
    self.button = tk.Button(self, text="SPIN", command=self.on_spin_press)
    self.button.pack(side=tk.RIGHT)

    self.increment_bet_button = tk.Button(
        self, text="+1", command=self.on_increment_bet_press)
    self.increment_bet_button.pack(side=tk.RIGHT)

    self.decrement_bet_button = tk.Button(
        self, text="-1", command=self.on_decrement_bet_press)
    self.decrement_bet_button.pack(side=tk.RIGHT)

    # Add the text boxes
    self.winner_paid_label = tk.Label(self, text="Winner paid: 0")
    self.winner_paid_label.pack()

    self.credits_label = tk.Label(self, text="Credits: 0")
    self.credits_label.pack()

    self.bet_label = tk.Label(self, text="Bet: 0")
    self.bet_label.pack()

    # Add the reels
    self.reel_labels = []
    for i in range(len(self.reels)):
      img = ImageTk.PhotoImage(
          self.reels[i].stops[self.current_stops[i]].image)
      reel_label = tk.Label(self, image=img)
      reel_label.image = img
      reel_label.pack()
      self.reel_labels.append(reel_label)

  def update_credits(self, credits):
    """ Update the credits box """

    self.credits_label.configure(text="Credits: %i" % credits)

  def update_bet(self, bet):
    """ Update the bet """

    self.bet_label.configure(text="Bet: %i" % bet)

  def update_winner_paid(self, winner_paid):
    """ Print the amount paid """

    self.winner_paid_label.configure(text="Winner paid: %i" % winner_paid)

  def clear_winner_paid(self):
    """ Blank out the winner paid box """

    self.winner_paid_label.configure(text="Winner paid: ")

  def show_reel_spin(self, result):
    """ Animate the spin """

    # Reset the reels
    for reel in range(len(self.reels)):
      self.reels[reel].reset(required_spins=((reel + 1) ** 2))

    # Which reels are still spinning?
    spinning_reels = range(len(self.reels))

    while len(spinning_reels) >= 1:
      for reel in spinning_reels:

        winning_symbol = result.reels[reel]

        im = ImageTk.PhotoImage(self.reels[reel].get_current_symbol().image)
        self.reel_labels[reel].configure(image=im)
        self.reel_labels[reel].image = im
        time.sleep(0.005)
        self.update()
        if not self.reels[reel].has_next(winning_symbol):
          # Remove from the list
          spinning_reels.remove(reel)
