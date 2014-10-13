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
# This example is inspired on Arduino Fade example.
# http://arduino.cc/en/Tutorial/Fade
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
pin = 3
brightness = 0
fadeAmount = 5

# Set pin 3 to be used as a PWM pin.
print 'Setting up pin %d' % pin
gpio.pinMode(pin, gpio.PWM)

print 'Fading pin %d now...' % pin
try:
    while(True):
        # Write brightness to the pin. The value must be between 0 and 255.
        gpio.analogWrite(pin, brightness)

        # Increment or decrement the brightness.
        brightness = brightness + fadeAmount

        # If the brightness has reached its maximum or minimum value swap
        # fadeAmount sign so we can start fading the led on the other direction.
        if brightness == 0 or brightness == 255:
            fadeAmount = -fadeAmount

        # Sleep for a while.
        time.sleep(0.03)

# When you get tired of seeing the led fading kill the loop with Ctrl-C.
except KeyboardInterrupt:
    # Leave the led turned off.
    print '\nCleaning up...'
    gpio.analogWrite(pin, 0)

    # Do a general cleanup. Calling this function is not mandatory.
    gpio.cleanup()
