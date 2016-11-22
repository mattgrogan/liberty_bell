import os.path as p

from liberty_bell.slot_machines.components.payline import Payline
from liberty_bell.slot_machines.components.slot_machine import Slot_Machine
from liberty_bell.slot_machines.components.symbol import Symbol
from liberty_bell.slot_machines.components.symbol_image_w import Symbol_Image_W

HEIGHT = 128
WIDTH = 128


class Liberty_Bell_Symbols(object):
  """ An enumerator class to hold all the symbol references """

  def __init__(self):
    """ Initialize the symbols for this game """

    current_dir = p.dirname(p.abspath(__file__))
    icon_dir = p.normpath(p.join(current_dir, "../icons"))

    bell_path = p.join(icon_dir, "Liberty_Bell.png")
    heart_path = p.join(icon_dir, "Hearts_96x96-32.png")
    diamond_path = p.join(icon_dir, "Diamonds_96x96-32.png")
    spade_path = p.join(icon_dir, "Spade_96x96-32.png")
    horseshoe_path = p.join(icon_dir, "Horseshoe_96x96-32.png")
    star_path = p.join(icon_dir, "Star_96x96-32.png")

    bell = Symbol_Image_W(bell_path, WIDTH, HEIGHT)
    heart = Symbol_Image_W(heart_path, WIDTH, HEIGHT)
    diamond = Symbol_Image_W(diamond_path, WIDTH, HEIGHT)
    spade = Symbol_Image_W(spade_path, WIDTH, HEIGHT)
    horseshoe = Symbol_Image_W(horseshoe_path, WIDTH, HEIGHT)
    star = Symbol_Image_W(star_path, WIDTH, HEIGHT)

    self.LIBERTY_BELL = Symbol(name="Liberty Bell", image=bell)
    self.HEART = Symbol(name="Heart", image=heart)
    self.DIAMOND = Symbol(name="Diamond", image=diamond)
    self.SPADE = Symbol(name="Spade", image=spade)
    self.HORSESHOE = Symbol(name="Horseshoe", image=horseshoe)
    self.STAR = Symbol(name="Star", image=star)


class Liberty_Bell_Machine(Slot_Machine):
  """ A slot machine based on the original Liberty Bell machine """

  def __init__(self, *args, **kwargs):
    """ Initialize the Liberty Bell slot Machine """

    super(Liberty_Bell_Machine, self).__init__(*args, **kwargs)

    self.name = "Liberty Bell"
    self.symbols = Liberty_Bell_Symbols()

    # Actual stops from Charles Fey's Liberty Bell machine
    # Source: Slot Machines: A Pictoral History of the First
    #  100 Years (Fifth Edition) by Marshall Fey

    stops0 = [self.symbols.HORSESHOE, self.symbols.DIAMOND,
              self.symbols.HORSESHOE, self.symbols.HORSESHOE,
              self.symbols.SPADE, self.symbols.LIBERTY_BELL,
              self.symbols.SPADE, self.symbols.HORSESHOE,
              self.symbols.HEART, self.symbols.HORSESHOE]

    stops1 = [self.symbols.HEART, self.symbols.SPADE,
              self.symbols.HORSESHOE, self.symbols.HORSESHOE,
              self.symbols.DIAMOND, self.symbols.HORSESHOE,
              self.symbols.SPADE, self.symbols.HORSESHOE,
              self.symbols.LIBERTY_BELL, self.symbols.HORSESHOE]

    stops2 = [self.symbols.STAR, self.symbols.DIAMOND,
              self.symbols.LIBERTY_BELL, self.symbols.SPADE,
              self.symbols.LIBERTY_BELL, self.symbols.DIAMOND,
              self.symbols.HEART, self.symbols.SPADE,
              self.symbols.DIAMOND, self.symbols.STAR]

    self.add_reel(stops=stops0)
    self.add_reel(stops=stops1)
    self.add_reel(stops=stops2)

    # Add the paylines to the payout table
    self.payout_table.append(Payline({self.symbols.LIBERTY_BELL: 3}, 20))
    self.payout_table.append(Payline({self.symbols.HEART: 3}, 16))
    self.payout_table.append(Payline({self.symbols.DIAMOND: 3}, 12))
    self.payout_table.append(Payline({self.symbols.SPADE: 3}, 8))
    self.payout_table.append(
        Payline({self.symbols.HORSESHOE: 2, self.symbols.STAR: 1}, 4))
    self.payout_table.append(Payline({self.symbols.HORSESHOE: 2}, 2))
