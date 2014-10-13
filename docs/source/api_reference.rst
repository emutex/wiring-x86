.. _workbook:

The Wiring-x86 API
==================

The ``wiring-x86`` module provides an unified API for all the platforms it
supports. In case of a platform-specific API was added it will be explicitly
mentioned in the documentation. 

Two classes are exposed my the module:

* ``GPIOEdison``
* ``GPIOGalileoGen2``
* ``GPIOGalileo``

The module is generally imported and intialised as follows::

    from wiringx86 import GPIOEdison as GPIO

    gpio = GPIO()



Constructor
-----------

.. py:function:: GPIO([debug])

   Create a new GPIO object.

   :param bool debug: Optional debug parameter.
   :rtype:            A GPIO object.


The ``GPIO()`` constructor is used to create a new gpio object::

   from wiringx86 import GPIOEdison as GPIO

   gpio = GPIO()

The ``debug`` constructor options can be used to enable the debug mode
showing the interaction with sysfs::

   gpio = GPIO(debug=False)


gpio.digitalWrite()
-------------------

.. function:: digitalWrite(pin, state)

   Configure a gpio pin for output.

   :param int pin:      Arduino pin number (0-19)
   :param string state: Pin state to be written (LOW-HIGH)

The ``digitalWrite()`` method is used to set the state for a given gpio
pin. The available states are ``high`` and ``low``. These are generally passed
as ``GPIO`` properties such as ``gpio.HIGH`` for convenience::

    gpio.digitalWrite(13, gpio.HIGH)

The GPIO pin is assumed to be configured as ``gpio.OUTPUT`` when writing.


gpio.digitalRead()
------------------

.. function:: digitalRead( pin)

   Read the state of a GPIO pin.

   :param int pin: Arduino pin number (0-19).
   :return:        Current value of the GPIO pin.
   :rtype:         int


Read the current state of a GPIO pin::

    state = gpio.digitalRead(pin)

The GPIO pin is assumed to be configured as ``gpio.INPUT``


gpio.analogWrite()
------------------


.. function:: analogWrite(pin, value)

   Write analog output (PWM) to a pin.

   :param int pin:   Arduino PWM pin number (3, 5, 6, 9, 10, 11)
   :param int value: The duty cycle: between 0 (always off) and 255 (always on).


The gpio pin is assumed to be configured as ``gpio.PWM``. Generates a PWM signal
with the desired duty cycle. The value must be in range 0-255.


gpio.analogRead()
-----------------

.. function:: analogRead(pin)

   Read analog input from the pin

   :param: int pin: Arduino analog pin number (14-19).
   :return:         Digital representation with 10 bits resolution
                    (range 0-1023) of voltage on the pin.

The GPIO pin is assumed to be configured as ``gpio.ANALOG_INPUT``. Returns
values in range 0-1023::

   value = gpio.analogRead(analogpin)


gpio.setPWMPeriod()
-------------------

.. function:: setPWMPeriod(pin, period)

   Set the PWM period.

   :param: int pin: Arduino PWM pin number (3, 5, 6, 9, 10, 11).
   :param: int period: PWM period in nanoseconds.


On the Galileo Gen2 all PWM channels share the same period. When this is set
all the PWM outputs are disabled for at least 1ms while the chip reconfigures
itself. The PWM pin is then ignored.

gpio.pinMode()
--------------

.. function:: pinMode(pin, mode)

   Set the mode of a GPIO pin.

   :param int pin:      Arduino pin number (0-19)
   :param string mode:  Pin mode. See below.

This function must be called before doing any other operation on the pin. It
sets up the muxing needed for the pin to put it in one of the following modes:

* OUTPUT: pin used as output. Use to write into it.
* INPUT: pin used as input (high impedance). Use to read from it.
* INPUT_PULLUP: pin used as input (pullup resistor). Use to read from it.
* INPUT_PULLDOWN: pin used as input (pulldown resistor). Use to read from it.
* ANALOG_INPUT: pin used as analog input (ADC).
* PWM: pin used as analog output (PWM).

For example::

    gpio.pinMode(pin, gpio.OUTPUT)


gpio.cleanup()
--------------

.. function:: cleanup(self)

   Do a general cleanup.

Close all open handlers for reading and writing. Unexport all exported GPIO
pins and unexport all exported PWM channels::

   gpio.cleanup()

Calling this function is not mandatory but it's recommended once you are
finished using the library and if it is being used with a larger application
that runs for a long period of time.
