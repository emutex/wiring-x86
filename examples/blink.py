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
state = gpio.HIGH
gpio.pinMode(pin, gpio.OUTPUT)

try:
    while(True):
        gpio.digitalWrite(pin, state)
        state = gpio.LOW if state == gpio.HIGH else gpio.HIGH
        time.sleep(0.5)
except:
    gpio.digitalWrite(pin, gpio.LOW)
    gpio.cleanup()
