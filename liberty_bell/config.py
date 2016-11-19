import ConfigParser

CONFIG_FILE = "/home/pi/github/liberty_bell/liberty_bell/config.ini"


class Config(object):
  """ Handle all the configuration options """

  def __init__(self, config_file=CONFIG_FILE):
    """ Read the configuration file and parse out the options """

    config = ConfigParser.ConfigParser()
    config.read(config_file)
    self.config = config

    # options
    self.default_credits = config.getint("OPTIONS", "default_credits")
    self.default_bet = config.getint("OPTIONS", "default_bet")
    self.max_bet = config.getint("OPTIONS", "max_bet")
    self.payout_delay_secs = config.getfloat("OPTIONS", "payout_delay_secs")

    # SEVEN SEGMENT DISPLAYS
    self.winner_paid_i2c = config.get("SEVENSEG_DISPLAYS", "winner_paid_i2c")
    self.credits_i2c = config.get("SEVENSEG_DISPLAYS", "credits_i2c")
    self.amount_bet_i2c = config.get("SEVENSEG_DISPLAYS", "amount_bet_i2c")

    # Convert to hex
    self.winner_paid_i2c = int(self.winner_paid_i2c, 16)
    self.credits_i2c = int(self.credits_i2c, 16)
    self.amount_bet_i2c = int(self.amount_bet_i2c, 16)

    # BUTTON GPIO PINS
    self.spin_pin = config.getint("BUTTON_PINS", "spin_button_pin")
    self.up_pin = config.getint("BUTTON_PINS", "up_button_pin")
    self.down_pin = config.getint("BUTTON_PINS", "down_button_pin")
    self.button1_pin = config.getint("BUTTON_PINS", "button1_pin")
    self.button2_pin = config.getint("BUTTON_PINS", "button2_pin")
    self.button3_pin = config.getint("BUTTON_PINS", "button3_pin")
    self.menu_pin = config.getint("BUTTON_PINS", "menu_button_pin")

    # BUTTON LED PINS
    self.spin_led = config.getint("BUTTON_LEDS", "spin_button_led")
    self.up_led = config.getint("BUTTON_LEDS", "up_button_led")
    self.down_led = config.getint("BUTTON_LEDS", "down_button_led")
    self.button1_led = config.getint("BUTTON_LEDS", "button1_led")
    self.button2_led = config.getint("BUTTON_LEDS", "button2_led")
    self.button3_led = config.getint("BUTTON_LEDS", "button3_led")

    # DISPLAYS
    self.display_1 = self.get_section_dict("DISPLAY_1")
    self.display_2 = self.get_section_dict("DISPLAY_2")
    self.display_3 = self.get_section_dict("DISPLAY_3")

    # MENU DISPLAY
    self.menu_display_i2c = config.get("MENU_DISPLAY", "i2c_address")
    self.menu_display_i2c = int(self.menu_display_i2c, 16)
    self.menu_display_reset = config.getint("MENU_DISPLAY", "reset")
    self.menu_display_width = config.getint("MENU_DISPLAY", "width")
    self.menu_display_height = config.getint("MENU_DISPLAY", "height")

    # SOUND
    self.sound_enabled = config.getint("SOUND", "enabled") == 1
    self.buzzer_pin = config.getint("SOUND", "buzzer_pin")

  def get_section_dict(self, section):
    """ Read in a sectiion as a dict """

    result = {}

    for opt in self.config.options(section):
      result[opt] = self.config.getint(section, opt)

    return result
