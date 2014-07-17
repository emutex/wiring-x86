# -*- coding: utf-8 -*-
"""
 Copyright © 2014, Emutex Ltd.
 All rights reserved.
 http://www.emutex.com

 Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>

 See license in LICENSE file.
"""

from wiringx86 import GPIOGalileoGen2 as GPIO

gpio = GPIO(debug=False)
pin = 13
button = 2

print 'Setting up pins %d and %d...' % (pin, button)
gpio.pinMode(pin, gpio.OUTPUT)
gpio.pinMode(button, gpio.INPUT)

print 'Reading from pin %d now...' % button
try:
    while(True):
        state = gpio.digitalRead(button)
        if state == 1:
            gpio.digitalWrite(pin, gpio.HIGH)
        else:
            gpio.digitalWrite(pin, gpio.LOW)

except KeyboardInterrupt:
    print '\nCleaning up...'
    gpio.digitalWrite(pin, gpio.LOW)
    gpio.cleanup()
