# Wiring-x86

Wiring-x86 is a Python module to use most Arduino functionalities on an
Intel® Galileo Gen2 board. It provides a simple API (much likely original
WiringPi-Python module) to talk to the GPIO pins in a very easily.

At the moment only basic GPIO functionality is enabled. That is:

*  Writing to a GPIO pin configured as output.
*  Reading from a GPIO pin configured as high impedance input.
*  Reading from a GPIO pin configured as pullup input.
*  Reading from a GPIO pin configured as pulldown input.

The Wiring-x86 module is meant to be used on Intel® Galileo Gen2 platform
with its original YOCTO Linux OS. For more information on the Intel® Galileo
Gen2 board and how to get this software go to
[Intel® Makers site][intel-makers].
Failing to do so will make the module not to work at all. The logic behind the
module is backed by Intel® Galileo Gen2 GPIO driver sysfs interface.

This is a simple example:

```python
 # Import time module to sleep between turning the led on and off.
 import time

 # Import the GPIOGalileoGen2 class from the wiringx86 module.
 from wiringx86 import GPIOGalileoGen2 as GPIO

 # Create a new instance of the GPIOGalileoGen2 class.
 # Setting debug=True would give you information about the interaction with sysfs
 gpio = GPIO(debug=False)
 pin = 13
 state = gpio.HIGH

 # Set the pin 13 to be used as an output GPIO pin
 gpio.pinMode(pin, gpio.OUTPUT)

 try:
     while(True):
         # Write a state to the pin. ON or OFF
         gpio.digitalWrite(pin, state)

         # Toggle the state
         state = gpio.LOW if state == gpio.HIGH else gpio.HIGH

         # Sleep for a bit
         time.sleep(0.5)

 # When you get tired of seeing the led blinking kill the loop with Ctrl-C.
 except KeyboardInterrupt:
     # Leave the led turned off
     gpio.digitalWrite(pin, gpio.LOW)

     # Do a general cleanup. Calling this function is not mandatory.
     gpio.cleanup()

```
______

[intel-makers]: https://communities.intel.com/community/makers
