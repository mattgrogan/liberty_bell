from __future__ import print_function
from datetime import datetime

import sys
sys.path.append("..")

from liberty_bell.events import Events
from liberty_bell.ui import Slot_UI
from ssd1351 import Adafruit_SSD1351
from PIL import ImageOps

from Adafruit_LED_Backpack import SevenSegment
import RPi.GPIO as GPIO

WINNER_PAID_LED = 0x70
CREDITS_LED = 0x71
AMOUNT_BET_LED = 0x72

SPIN_BUTTON_GPIO = 18

# OLED
SSD1351_WIDTH = 128
SSD1351_HEIGHT = 128
RST = 24
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Set up the GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(SPIN_BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)

class Slot_RPI_UI(Slot_UI):
    """ Raspberry PI UI for the slot machine """

    def __init__(self, *args, **kwargs):
        """ Initialize the UI """

        super(Slot_RPI_UI, self).__init__(*args, **kwargs)

    	# Set up the winner paid LED
    	self.winner_paid_led = SevenSegment.SevenSegment(address=WINNER_PAID_LED)
    	self.winner_paid_led.begin()
    	self.winner_paid_led.clear()
    	self.winner_paid_led.write_display()

    	# Set up the credits LED
    	self.credits_led = SevenSegment.SevenSegment(address=CREDITS_LED)
    	self.credits_led.begin()
    	self.credits_led.clear()
    	self.credits_led.write_display()

    	# Set up the amount bet LED
    	self.amount_bet_led = SevenSegment.SevenSegment(address=AMOUNT_BET_LED)
    	self.amount_bet_led.begin()
    	self.amount_bet_led.clear()
    	self.amount_bet_led.write_display()

    	# Set up the GPIO buttons
    	GPIO.add_event_detect(SPIN_BUTTON_GPIO, GPIO.RISING, callback=self.on_gpio_spin_press, bouncetime=1000)
    	#	GPIO.add_event_detect(SPIN_BUTTON_GPIO, self.on_gpio_spin_button, bouncetime=200)
    	self.last_spin_interrupt = False

        self.credits = 0
        self.bet = 0
        self.winner_paid = 0

        # Set up the OLED screens
        self.oleds = []
        self.oleds.append(Adafruit_SSD1351(SSD1351_WIDTH,
                                 SSD1351_HEIGHT,
                                 rst=RST,
                                 dc=DC,
                                 spi_port=SPI_PORT,
                                 spi_device=SPI_DEVICE))

        self.oleds[0].begin()
    	self.oleds[0].clear_buffer()
    	self.oleds[0].display()

    def mainloop(self):
        """ The main loop for the game """

        continue_playing = True

        while (continue_playing):
            text = "Choose an option: S: Spin | I: increase bet | D: decrease bet | Q: quit [S] "
            option = raw_input(text)

            if option in ["S", "s"]:
    		# Reset the winnings
    		self.winner_paid_led.clear()
    		self.winner_paid_led.write_display()
                self.on_spin_press()
            elif option in ["I", "i"]:
                self.on_increment_bet_press()
            elif option in ["D", "d"]:
                self.on_decrement_bet_press()
            elif option in ["Q", "q"]:
                continue_playing = False
            else:
                self.on_spin_press()

            print("\n")

    def print_status(self):
        """ Print the status on one line """
        print("Credits: %i | Bet: %i | Winner paid: %i " %
              (self.credits, self.bet, self.winner_paid))

    def update_credits(self, credits):
        """ Update the credits box """

        self.credits = credits
        self.print_status()
    	self.credits_led.clear()
    	self.credits_led.print_float(credits, decimal_digits=0)
    	self.credits_led.write_display()

    def update_bet(self, bet):
        """ Update the bet """

        self.bet = bet
        self.print_status
    	self.amount_bet_led.clear()
    	self.amount_bet_led.print_float(bet, decimal_digits=0)
    	self.amount_bet_led.write_display()

    def update_winner_paid(self, winner_paid):
        """ Print the amount paid """

        self.winner_paid = winner_paid
        self.print_status()
    	self.winner_paid_led.clear()
    	self.winner_paid_led.print_float(winner_paid, decimal_digits=0)
    	self.winner_paid_led.write_display()

    def clear_winner_paid(self):
        """ Blank out the winner paid amount """


	    self.winner_paid_led.clear()
	    self.winner_paid_led.write_display()


    def on_gpio_spin_press(self, e):
	""" Call on_spin_press """

	   self.on_spin_press()

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

                im = self.reels[reel].get_current_symbol().image

                # Resize for the screen
                # TODO: make sure the width and height and border tuples are in the correct order
                # it might work only because we're dealing with squares
                if im.size != (SSD1351_WIDTH, SSD1351_HEIGHT):
                    width_diff = SSD1351_WIDTH - im.size[0]
                    height_diff = SSD1351_HEIGHT - im.size[1]
                    border_size = (width_diff / 2, width_diff / 2, height_diff / 2, height_diff / 2)
                    im = ImageOps.expand(im, border = border_size)

                # Make sure it's RGB
                im = im.convert("RGB")

                # Load and display
                self.oleds[reel].load_image(im)
                self.oleds[reel].display()

                time.sleep(0.005)

                # Remove the reel from the list if it has stopped
                if not self.reels[reel].has_next(winning_symbol):
                    spinning_reels.remove(reel)
