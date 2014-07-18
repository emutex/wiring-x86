.. _workbook:

The Wiring-x86 API
==================

The ``GPIOGalileoGen2`` class is the main class exposed by the ``wiring-x86``
module.

In future releases other Intel® Quark® class boards will be supported.

The module is generally imported and intialised as follows::

    from wiringx86 import GPIOGalileoGen2 as GPIO

    gpio = GPIO()



Constructor
-----------

.. py:function:: GPIO([debug])

   Create a new GPIO object.

   :param bool debug: Optional debug parameter.
   :rtype:            A GPIO object.


The ``GPIO()`` constructor is used to create a new gpio object::

   from wiringx86 import GPIOGalileoGen2 as GPIO

   gpio = GPIO()

The ``debug`` constructor options can be used to enables the debug mode
showing the interaction with sysfs::

   gpio = GPIO(debug=False)


gpio.digitalWrite()
-------------------

.. function:: digitalWrite(pin, state)

   Configure a gpio pin for output.

   :param int pin:      Arduino pin number (0-20)
   :param string state: Pin state to be written (LOW-HIGH)

The ``digitalWrite()`` method is used to set the state for a given gpio
pin. The available states are ``high`` and ``low``. These are generally passed as ``GPIO`` properties such as ``gpio.HIGH`` for converience::

    gpio.digitalWrite(13, gpio.HIGH)
