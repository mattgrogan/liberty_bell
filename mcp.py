import time

import Adafruit_GPIO as GPIO
import Adafruit_GPIO.MCP230xx as adafruit_mcp

# Use busnum = 0 for older Raspberry Pi's (256MB)
#mcp = adafruit_mcp.MCP23008()
# Use busnum = 1 for new Raspberry Pi's (512MB with mounting holes)
mcp = adafruit_mcp.MCP23008(address=0x20)


# Set pin 3 to input with the pullup resistor enabled
mcp.setup(0, GPIO.OUT)


# Python speed test on output 0 toggling at max speed
while (True):
  print "high"
  mcp.output(0, GPIO.HIGH)  # Pin 0 High
  time.sleep(1)
  print "low"
  mcp.output(0, GPIO.LOW)  # Pin 1 Low  time.sleep(0.1)
  time.sleep(1)
