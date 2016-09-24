import argparse
import sys

from front_controller import Front_Controller

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Play a slot machine.")
  parser.add_argument("-t", action="store_true")
  args = parser.parse_args()

  controller = Front_Controller()

  controller.start()
