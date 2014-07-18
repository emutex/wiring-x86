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
pin = 3
brightness = 0
fadeAmount = 5

print 'Setting up pin %d' % pin
gpio.pinMode(pin, gpio.PWM)

print 'Fading pin %d now...' % pin
try:
    while(True):
        gpio.analogWrite(pin, brightness)

        brightness = brightness + fadeAmount

        if brightness == 0 or brightness == 255:
            fadeAmount = -fadeAmount

        time.sleep(0.03)

except KeyboardInterrupt:
    print '\nCleaning up...'
    gpio.analogWrite(pin, 0)
    gpio.cleanup()
