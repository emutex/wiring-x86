Wiring-x86
==========

Wiring-x86 is a Python module that lets you use Arduino like
functionality on an Intel® Galileo Gen2 board. It provides a simple API
(similar to the WiringPi module) to talk to the GPIO pins on the board.

.. image:: https://raw.githubusercontent.com/emutex/wiring-x86/master/docs/source/_images/galileo1.jpg

At the momment the Wiring-x86 library provides support to:

-  Writing to a GPIO pin configured as output.
-  Reading from a GPIO pin configured as high impedance input.
-  Reading from a GPIO pin configured as pullup input.
-  Reading from a GPIO pin configured as pulldown input.
-  Reading from a GPIO pin configured as analog input (ADC).
-  Writing to a GPIO pin configured as analog output (PWM).

Here is a simple example::

    # Import the time module enable sleeps between turning the led on and off.
    import time

    # Import the GPIOGalileoGen2 class from the wiringx86 module.
    from wiringx86 import GPIOGalileoGen2 as GPIO

    # Create a new instance of the GPIOGalileoGen2 class.
    # Setting debug=True gives information about the interaction with sysfs.
    gpio = GPIO(debug=False)
    pin = 13
    state = gpio.HIGH

    # Set pin 13 to be used as an output GPIO pin.
    print 'Setting up pin %d' % pin
    gpio.pinMode(pin, gpio.OUTPUT)


    print 'Blinking pin %d now...' % pin
    try:
        while(True):
            # Write a state to the pin. ON or OFF.
            gpio.digitalWrite(pin, state)

            # Toggle the state.
            state = gpio.LOW if state == gpio.HIGH else gpio.HIGH

            # Sleep for a while.
            time.sleep(0.5)

    # When you get tired of seeing the led blinking kill the loop with Ctrl-C.
    except KeyboardInterrupt:
        # Leave the led turned off.
        print '\nCleaning up...'
        gpio.digitalWrite(pin, gpio.LOW)

        # Do a general cleanup. Calling this function is not mandatory.
        gpio.cleanup()

The Wiring-x86 module is meant to be used on Intel® Galileo Gen2
platform with its original YOCTO Linux OS. For more information on the
Intel® Galileo Gen2 board and how to get this software go to `Intel®
Makers site <https://communities.intel.com/community/makers>`_. This
module will only work with that combination of board and OS since it
uses the Intel® Galileo Gen2 GPIO driver sysfs interface.

