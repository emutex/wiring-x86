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
state = gpio.HIGH
pins = 20

print 'Setting up all pins...'
for pin in range(0, pins):
    gpio.pinMode(pin, gpio.OUTPUT)

print 'Blinking all pins now...'
try:
    while(True):
        for pin in range(0, pins):
            gpio.digitalWrite(pin, state)
        state = gpio.LOW if state == gpio.HIGH else gpio.HIGH
        time.sleep(0.5)

except KeyboardInterrupt:
    print '\nCleaning up...'
    for pin in range(0, pins):
        gpio.digitalWrite(pin, gpio.LOW)
    gpio.cleanup()
