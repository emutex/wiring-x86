# -*- coding: utf-8 -*-
#
# Copyright © 2014, Emutex Ltd.
# All rights reserved.
# http://www.emutex.com
#
# Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>
#
# See license in LICENSE.txt file.
#
# This example is inspired on Arduino Analog Input example.
# http://arduino.cc/en/Tutorial/AnalogInput
#
# This example will work "out of the box" on an Intel® Edison board. If
# you are using a different board such as an Intel® Galileo Gen2, just change the
# import below. wiringx86 uses the same API for all the boards it supports.

# Import the time module enable sleeps between turning the led on and off.
import time

# Import the GPIOEdison class from the wiringx86 module.
from wiringx86 import GPIOEdison as GPIO

# Create a new instance of the GPIOEdison class.
# Setting debug=True gives information about the interaction with sysfs.
gpio = GPIO(debug=False)
pin = 13
analogpin = 14

print 'Setting up all pins...'

# Set pin 14 to be used as an analog input GPIO pin.
gpio.pinMode(analogpin, gpio.ANALOG_INPUT)

# Set pin 13 to be used as an output GPIO pin.
gpio.pinMode(pin, gpio.OUTPUT)

print 'Analog reading from pin %d now...' % analogpin
try:
    while(True):
        # Read the voltage on pin 14
        value = gpio.analogRead(analogpin)

        # Turn ON pin 13
        gpio.digitalWrite(pin, gpio.HIGH)

        # Sleep for a while depending on the voltage we just read. The higher
        # the voltage the more we sleep.
        time.sleep(value / 1023.0)

        # Turn OFF pin 13
        gpio.digitalWrite(pin, gpio.LOW)

        # Sleep for a while depending on the voltage we just read. The higher
        # the voltage the more we sleep.
        time.sleep(value / 1023.0)

# When you get tired of seeing the led blinking kill the loop with Ctrl-C.
except KeyboardInterrupt:
    # Leave the led turned off.
    print '\nCleaning up...'
    gpio.digitalWrite(pin, gpio.LOW)

    # Do a general cleanup. Calling this function is not mandatory.
    gpio.cleanup()
