import argparse
import sys

from application_controller import Application_Controller

if __name__ == '__main__':

  parser = argparse.ArgumentParser(description="Play a slot machine.")
  parser.add_argument("-t", action="store_true")
  args = parser.parse_args()

  controller = Application_Controller()

  controller.start()
