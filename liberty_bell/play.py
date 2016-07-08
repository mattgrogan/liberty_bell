from __future__ import print_function
import argparse
from controller import Slot_Game_Controller

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Play a slot machine.")

    parser.add_argument("--ui", choices=["text", "gui", "rpi"], required=True)

    args = parser.parse_args()

    if args.ui == "text":
        ui = "TEXT_UI"
    elif args.ui == "gui":
        ui = "GUI_UI"
    elif args.ui == "rpi":
        ui = "RPI_UI"
    else:
        raise ValueError("Invalid user interface specified.")

    controller = Slot_Game_Controller(ui)
