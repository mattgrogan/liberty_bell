import os
from components.payline import Payline
from components.slot_machine import Slot_Machine
from components.symbol import Symbol



class Liberty_Bell_Symbols(object):
  """ An enumerator class to hold all the symbol references """

  def __init__(self):
    """ Initialize the symbols for this game """

    current_dir = os.path.dirname(os.path.abspath(__file__))

    bell = os.path.normpath(os.path.join(current_dir, "../icons/Liberty_Bell_128x128.png"))
    heart = os.path.normpath(os.path.join(current_dir, "../icons/Hearts_96x96-32.png"))
    diamond = os.path.normpath(os.path.join(current_dir, "../icons/Diamonds_96x96-32.png"))
    spade = os.path.normpath(os.path.join(current_dir, "../icons/Spade_96x96-32.png"))
    horseshoe = os.path.normpath(os.path.join(current_dir, "../icons/Horseshoe_96x96-32.png"))
    star = os.path.normpath(os.path.join(current_dir, "../icons/Star_96x96-32.png"))

    self.LIBERTY_BELL = Symbol(name="Liberty Bell", img_path=bell)
    self.HEART = Symbol(name="Heart", img_path=heart)
    self.DIAMOND = Symbol(name="Diamond", img_path=diamond)
    self.SPADE = Symbol(name="Spade", img_path=spade)
    self.HORSESHOE = Symbol(name="Horseshoe", img_path=horseshoe)
    self.STAR = Symbol(name="Star", img_path=star)


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
