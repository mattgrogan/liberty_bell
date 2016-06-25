""" Package liberty bell into a single namespace """

from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from liberty_bell.machine import Slot_Machine
from liberty_bell.events import Events
from liberty_bell.symbol import Symbol
from liberty_bell.ui import Slot_UI


from liberty_bell.reel import Reel
from liberty_bell.slot_machines import Liberty_Bell_Symbols
from liberty_bell.slot_machines import Liberty_Bell_Machine
from liberty_bell.payout import Payline, Payout_Table
from liberty_bell.controller import Slot_Game_Controller

symbols = Liberty_Bell_Symbols()
