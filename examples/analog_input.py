# -*- coding: utf-8 -*-
"""
 Copyright © 2014, Emutex Ltd.
 All rights reserved.
 http://www.emutex.com

 Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>

 See license in LICENSE file.
"""

import time
from wiringx86 import GPIOGalileoGen2 as GPIO

gpio = GPIO(debug=False)
pin = 13
analogpin = 14

print 'Setting up all pins...'
gpio.pinMode(analogpin, gpio.ANALOG_INPUT)
gpio.pinMode(pin, gpio.OUTPUT)

print 'Analog reading from pin %d now...' % analogpin
try:
    while(True):
        value = gpio.analogRead(analogpin)
        gpio.digitalWrite(pin, gpio.HIGH)
        time.sleep(value / 1023.0)
        gpio.digitalWrite(pin, gpio.LOW)
        time.sleep(value / 1023.0)

except KeyboardInterrupt:
    print '\nCleaning up...'
    gpio.digitalWrite(pin, gpio.LOW)
    gpio.cleanup()
