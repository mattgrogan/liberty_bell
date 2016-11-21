import os.path as p

from components.payline import Payline
from components.slot_machine import Slot_Machine
from components.symbol import Symbol
from components.symbol_image_w import Symbol_Image_W

HEIGHT = 128
WIDTH = 128


class Gold_Award_Symbols(object):
  """ An enumerator class to hold all the symbol references """

  def __init__(self):
    """ Initialize the symbols for this game """

    current_dir = p.dirname(p.abspath(__file__))
    icon_dir = p.normpath(p.join(current_dir, "../icons/"))

    lemon_path = p.join(icon_dir, "Lemon_96x96-32.png")
    cherry_path = p.join(icon_dir, "Cherry_96x96-32.png")
    orange_path = p.join(icon_dir, "Orange_96x96-32.png")
    plum_path = p.join(icon_dir, "Plum_96x96-32.png")
    bell_path = p.join(icon_dir, "Bell_96x96-32.png")
    gold_path = p.join(icon_dir, "Gold Bar_96x96-32.png")
    bar_path = p.join(icon_dir, "Bar_96x96-32.png")

    lemon = Symbol_Image_W(lemon_path, WIDTH, HEIGHT)
    cherry = Symbol_Image_W(cherry_path, WIDTH, HEIGHT)
    orange = Symbol_Image_W(orange_path, WIDTH, HEIGHT)
    plum = Symbol_Image_W(plum_path, WIDTH, HEIGHT)
    bell = Symbol_Image_W(bell_path, WIDTH, HEIGHT)
    gold = Symbol_Image_W(gold_path, WIDTH, HEIGHT)
    bar = Symbol_Image_W(bar_path, WIDTH, HEIGHT)

    self.LEMON = Symbol(name="Lemon", image=lemon)
    self.CHERRY = Symbol(name="Cherry", image=cherry)
    self.ORANGE = Symbol(name="Orange", image=orange)
    self.PLUM = Symbol(name="Plum", image=plum)
    self.BELL = Symbol(name="Bell", image=bell)
    self.GOLD = Symbol(name="Gold", image=gold)
    self.BAR = Symbol(name="Bar", image=bar)


class Gold_Award_Machine(Slot_Machine):
  """ A slot machine based on the Gold Award machine """

  def __init__(self, *args, **kwargs):
    """ Initialize the slot Machine """

    super(Gold_Award_Machine, self).__init__(*args, **kwargs)

    self.name = "Gold Award"
    self.symbols = Gold_Award_Symbols()

    # Actual stops from Mill's Gold Award (c.1935)
    # Source: Slot Machines: A Pictoral History of the First
    #  100 Years (Fifth Edition) by Marshall Fey

    stops0 = [self.symbols.LEMON, self.symbols.CHERRY,
              self.symbols.ORANGE, self.symbols.PLUM,
              self.symbols.CHERRY, self.symbols.BELL,
              self.symbols.LEMON, self.symbols.CHERRY,
              self.symbols.GOLD, self.symbols.BAR,
              self.symbols.CHERRY, self.symbols.LEMON,
              self.symbols.CHERRY, self.symbols.ORANGE,
              self.symbols.BAR, self.symbols.LEMON,
              self.symbols.CHERRY, self.symbols.GOLD,
              self.symbols.ORANGE, self.symbols.PLUM
              ]

    stops1 = [self.symbols.PLUM, self.symbols.CHERRY,
              self.symbols.BELL, self.symbols.ORANGE,
              self.symbols.GOLD, self.symbols.CHERRY,
              self.symbols.ORANGE, self.symbols.BELL,
              self.symbols.PLUM, self.symbols.CHERRY,
              self.symbols.CHERRY, self.symbols.BAR,
              self.symbols.ORANGE, self.symbols.CHERRY,
              self.symbols.CHERRY, self.symbols.PLUM,
              self.symbols.BELL, self.symbols.CHERRY,
              self.symbols.PLUM, self.symbols.ORANGE
              ]

    stops2 = [self.symbols.ORANGE, self.symbols.LEMON,
              self.symbols.BAR, self.symbols.PLUM,
              self.symbols.BELL, self.symbols.ORANGE,
              self.symbols.GOLD, self.symbols.PLUM,
              self.symbols.LEMON, self.symbols.ORANGE,
              self.symbols.PLUM, self.symbols.BELL,
              self.symbols.BELL, self.symbols.ORANGE,
              self.symbols.BAR, self.symbols.LEMON,
              self.symbols.PLUM, self.symbols.ORANGE,
              self.symbols.BELL, self.symbols.PLUM,
              ]

    self.add_reel(stops=stops0)
    self.add_reel(stops=stops1)
    self.add_reel(stops=stops2)

    # Add the paylines to the payout table
    self.payout_table.append(Payline({self.symbols.CHERRY: 2}, 3))
    self.payout_table.append(
        Payline({self.symbols.CHERRY: 2, self.symbols.LEMON: 1}, 5))
    self.payout_table.append(
        Payline({self.symbols.CHERRY: 2, self.symbols.BELL: 1}, 5))

    self.payout_table.append(Payline({self.symbols.ORANGE: 3}, 10))
    self.payout_table.append(
        Payline({self.symbols.ORANGE: 2, self.symbols.BAR: 1}, 10))

    self.payout_table.append(Payline({self.symbols.PLUM: 3}, 14))
    self.payout_table.append(
        Payline({self.symbols.PLUM: 2, self.symbols.BAR: 1}, 14))

    self.payout_table.append(Payline({self.symbols.BELL: 3}, 18))
    self.payout_table.append(
        Payline({self.symbols.BELL: 2, self.symbols.BAR: 1}, 18))

    self.payout_table.append(Payline({self.symbols.GOLD: 3}, 75))

    self.payout_table.append(Payline({self.symbols.BAR: 3}, 120))
