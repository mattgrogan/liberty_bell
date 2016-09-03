import time

import RPi.GPIO as GPIO


class Buzzer(object):
  """ Plays sound if enabled """

  def __init__(self, buzzer_pin, sound_enabled):
    """ Initialize the buzzer """

    self.gpio_pin = buzzer_pin
    self.sound_enabled = sound_enabled

    # Initialize the GPIO pin
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio_pin, GPIO.OUT)

    self.pwm = GPIO.PWM(self.gpio_pin, 100)
    self.pwm.start(0)

  def tone(self, frequency, duration):
    """ Play a tone of frequency for duration in seconds """

    if not self.sound_enabled:
      return

    if(frequency == 0):
      time.sleep(duration)
      return

    self.pwm.ChangeDutyCycle(0.50)
    self.pwm.ChangeFrequency(frequency)
    time.sleep(duration)
    self.pwm.ChangeDutyCycle(0.00)

  def increment_tone(self):
    """ Tone for incrementing the payout """

    self.tone(100, 0.05)

  def lose_tone(self):
    """ Play a lose tone """

    self.tone(261, 0.10)
    self.tone(138, 0.20)

  def button_tone(self):
    """ Play a click tone """

    self.tone(783, 0.05)
    self.tone(987, 0.05)
    self.tone(523, 0.10)
    self.tone(1760, 0.05)
