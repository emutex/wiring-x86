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
# This example is inspired on Arduino Button example.
# http://arduino.cc/en/Tutorial/Button
#
# This example will work "out of the box" on an Intel® Edison board. If
# you are using a different board such as an Intel® Galileo Gen2, just change the
# import below. wiringx86 uses the same API for all the boards it supports.

# Import the GPIOEdison class from the wiringx86 module.
from wiringx86 import GPIOEdison as GPIO

# Create a new instance of the GPIOEdison class.
# Setting debug=True gives information about the interaction with sysfs.
gpio = GPIO(debug=False)
pin = 13
button = 2

print 'Setting up pins %d and %d...' % (pin, button)

# Set pin 13 to be used as an output GPIO pin.
gpio.pinMode(pin, gpio.OUTPUT)

# Set pin 2 to be used as an input GPIO pin.
gpio.pinMode(button, gpio.INPUT)

print 'Reading from pin %d now...' % button
try:
    while(True):
        # Read the state of the button
        state = gpio.digitalRead(button)

        # If the button is pressed turn ON pin 13
        if state == 1:
            gpio.digitalWrite(pin, gpio.HIGH)

        # If the button is not pressed turn OFF pin 13
        else:
            gpio.digitalWrite(pin, gpio.LOW)

# Kill the loop with Ctrl-C.
except KeyboardInterrupt:
    # Leave the led turned off.
    print '\nCleaning up...'
    gpio.digitalWrite(pin, gpio.LOW)

    # Do a general cleanup. Calling this function is not mandatory.
    gpio.cleanup()
