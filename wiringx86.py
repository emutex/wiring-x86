# -*- coding: utf-8 -*-
#
# Copyright © 2014, Emutex Ltd.
# All rights reserved.
# http://www.emutex.com
#
# Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>
# Author: Dave Hunt <dave@emutex.com>
#
# See license in LICENSE.txt file.
#
# Wiring-x86 is a Python module that lets you use Arduino like functionality
# on
#  Intel® Gaileo
#  Intel® Gaileo Gen2
#  Intel® Edison

import datetime
import os

INPUT = 'in'
INPUT_PULLUP = 'in_pullup'
INPUT_PULLDOWN = 'in_pulldown'
OUTPUT = 'out'
ANALOG_INPUT = 'analog_input'
PWM = 'pwm'
LOW = 'low'
HIGH = 'high'
NONE = 'in'
DRIVE_STRONG = 'strong'
DRIVE_HIZ = 'hiz'
MODE_0 = 'mode0'
MODE_1 = 'mode1'
MODE_2 = 'mode2'
MODE_3 = 'mode3'
MODE_4 = 'mode4'
MODE_5 = 'mode5'
ALL_MODES = (MODE_0, MODE_1, MODE_2, MODE_3, MODE_4, MODE_5)


class GPIOBase(object):

    def __init__(self, debug=False):
        """Constructor

        Args:
            debug: enables the debug mode showing the interaction with sysfs

        """
        self.debug = debug
        self.pins_in_use = []
        self.gpio_handlers = {}
        self.exported_pwm = []
        self.enabled_pwm = {}

        if self.has_pinmux():
            self._export_pin(self.pinmux)
            self._set_direction(self.pinmux, self.HIGH)

    def has_pinmux(self):
        return hasattr(self, 'pinmux')

    def pinMode(self, pin, mode):
        """Set mode to GPIO pin`.

        This function must be called before doing any other operation on the
        pin. It also sets up the muxing needed in the board for the pin to
        behave as the user wants to.

        Args:
            pin: Arduino pin number (0-19)
            mode: pin mode must be:
                OUTPUT:         Pin used as output. Use to write into it.
                INPUT:          Pin used as input (high impedance). Use to read
                                from it.
                INPUT_PULLUP:   Pin used as input (pullup resistor). Use to read
                                from it.
                INPUT_PULLDOWN: Pin used as input (pulldown resistor). Use to
                                read from it.
                ANALOG_INPUT:   Pin used as analog input (ADC).
                PWM:            Pin used as analog output (PWM).

        """
        if pin not in self.GPIO_MAPPING:
            return False

        if self.has_pinmux():
            self._set_direction(self.pinmux, self.LOW)

        mux = self._select_muxing(mode, pin)
        if mux is None:
            return False

        linux_pin = self.GPIO_MAPPING[pin]
        self._export_pin(linux_pin)

        # In these two cases we open file handlers to write directly into them.
        # That makes it faster than going through sysfs.
        # No bother with PWM.
        if mode == ANALOG_INPUT:
            adc = self.ADC_MAPPING[pin]
            self._open_analog_handler(linux_pin, adc)
        elif mode in (OUTPUT, INPUT, INPUT_PULLUP, INPUT_PULLDOWN):
            self._open_digital_handler(linux_pin)

        # Walk through the muxing table and set the pins to their values. This
        # is the actual muxing.
        for vpin, value in mux:
            self._export_pin(vpin)

            self._set_direction(vpin, value)
            if value == NONE:
                self._set_drive(vpin, DRIVE_HIZ)
            elif value in (HIGH, LOW):
                self._set_drive(vpin, DRIVE_STRONG)
                self._write_value(vpin, value)
            elif value in ALL_MODES:
                self._muxmode(vpin, value)

        if mode == OUTPUT:
            self._set_direction(linux_pin, OUTPUT)
            self._set_drive(linux_pin, DRIVE_STRONG)
            self._write_value(linux_pin, LOW)
        elif mode in (INPUT, INPUT_PULLUP, INPUT_PULLDOWN):
            self._set_direction(linux_pin, INPUT)
        elif mode == PWM:
            self._init_pwm(pin)

        if self.has_pinmux():
            self._set_direction(self.pinmux, self.HIGH)

        return True

    def digitalWrite(self, pin, state):
        """Write a value to a GPIO pin.

        The GPIO pin is assumed to be configured as OUTPUT

        Args:
            pin: Arduino pin number (0-19)
            state: pin state to be written (LOW-HIGH)

        """
        if pin not in self.GPIO_MAPPING:
            return
        self._write_value_to_handler(self.GPIO_MAPPING[pin], state)

    def digitalRead(self, pin):
        """Read GPIO pin's state.

        The GPIO pin is assumed to be configured as INPUT

        Args:
            pin: Arduino pin number (0-19)

        Returns:
            Current value of the GPIO pin as an Integer

        """
        if pin not in self.GPIO_MAPPING:
            return
        handler = self.gpio_handlers[self.GPIO_MAPPING[pin]]
        state = handler.read()
        handler.seek(0)
        return int(state.strip())

    def analogWrite(self, pin, value):
        """Write analog output (PWM)

        The GPIO pin is assumed to be configured as PWM. Generates a PWM
        signal with the desired duty cycle. The value must be in range 0-255.

        Args:
            pin: Arduino PWM pin number (3, 5, 6, 9, 10, 11)
            value: the duty cycle: between 0 (always off) and 255 (always on)

        """
        if pin not in self.PWM_MAPPING:
            return

        if value < 0:
            value = 0
        elif value > 255:
            value = 255

        pwm = self.PWM_MAPPING[pin]
        if not self.enabled_pwm.get(pwm, False):
            self._enable_pwm(pwm)
        self._set_pwm_duty_cycle(pwm, self._get_pwm_period(pin) * value / 255)

    def analogRead(self, pin):
        """Read analog input from the pin

        The GPIO pin is assumed to be configured as ANALOG_INPUT.
        Returns values in range 0-1023

        Args:
            pin: Arduino analog pin number (14-19)

        Returns:
            Digital representation with 10 bits resolution (range 0-1023) of
            voltage on the pin.

        """
        if pin not in self.ADC_MAPPING:
            return
        handler = self.gpio_handlers[self.GPIO_MAPPING[pin]]
        voltage = handler.read()
        handler.seek(0)
        # ADC chip on the board reports voltages with 12 bits resolution.
        # To convert it to 10 bits just shift right 2 bits.
        return int(voltage.strip()) >> 2

    def setPWMPeriod(self, pin, period):
        """Set the PWM period

        Check if the period is valid for the current system and proceed to
        set the new period.

        Args:
            pin: Arduino PWM pin number (3, 5, 6, 9, 10, 11)
            period: period in nanoseconds

        """
        if period < self.PWM_MIN_PERIOD or period > self.PWM_MAX_PERIOD:
            return

        self._set_pwm_period(pin, period)

    def cleanup(self):
        """Do a general cleanup.

        Close all open handlers for reading and writing.
        Unexport all exported GPIO pins.
        Unexport all exported PWM channels.

        Calling this function is not mandatory but it's recommended once you
        are done using the library if it's being used with a larger
        application that runs for a long period of time.

        """
        for pin in self.pins_in_use:
            self._unexport_pin(pin)
        del self.pins_in_use[:]

        for handler in self.gpio_handlers.values():
            handler.close()
        self.gpio_handlers.clear()

        for pwm in self.exported_pwm:
            self._unexport_pwm(pwm)
        del self.exported_pwm[:]
        self.enabled_pwm.clear()

    def _select_muxing(self, mode, pin):
        if mode == OUTPUT:
            return self.GPIO_MUX_OUTPUT[pin]
        elif mode == INPUT:
            return self.GPIO_MUX_INPUT[pin]
        elif mode == INPUT_PULLUP:
            return self.GPIO_MUX_INPUT_PULLUP[pin]
        elif mode == INPUT_PULLDOWN:
            return self.GPIO_MUX_INPUT_PULLDOWN[pin]
        elif mode == ANALOG_INPUT and pin in self.ADC_MAPPING:
            return self.GPIO_MUX_ANALOG_INPUT[pin]
        elif mode == PWM and pin in self.PWM_MAPPING:
            return self.GPIO_MUX_PWM[pin]
        return None

    def _open_digital_handler(self, linux_pin):
        try:
            f = open('/sys/class/gpio/gpio%d/value' % linux_pin, 'r+')
            self.gpio_handlers[linux_pin] = f
        except:
            print "Failed opening digital value file for pin %d" % linux_pin

    def _open_analog_handler(self, linux_pin, adc):
        try:
            f = open('/sys/bus/iio/devices/iio:device%d/in_voltage%d_raw' % (self.adc_iio_device, adc), 'r+')
            self.gpio_handlers[linux_pin] = f
        except:
            print "Failed opening analog value file for pin %d" % linux_pin

    def _write_value(self, linux_pin, state):
        value = 1
        if state == LOW:
            value = 0
        cmd = 'echo %d > /sys/class/gpio/gpio%d/value' % (value, linux_pin)
        self._exec_cmd(self._write_value.__name__, cmd)

    def _write_value_to_handler(self, linux_pin, state):
        handler = self.gpio_handlers[linux_pin]
        value = '0' if state == LOW else '1'
        handler.write(value)
        handler.seek(0)

    def _set_direction(self, linux_pin, direction):
        dirfile = '/sys/class/gpio/gpio%d/direction' % linux_pin
        cmd = 'test -f %s && echo %s > %s 2>&1' % (dirfile, direction, dirfile)
        self._exec_cmd(self._set_direction.__name__, cmd)

    def _export_pin(self, linux_pin):
        self.pins_in_use.append(linux_pin)
        cmd = 'echo %d > /sys/class/gpio/export 2>&1' % linux_pin
        self._exec_cmd(self._export_pin.__name__, cmd)

    def _unexport_pin(self, linux_pin):
        cmd = 'echo %d > /sys/class/gpio/unexport 2>&1' % linux_pin
        self._exec_cmd(self._unexport_pin.__name__, cmd)

    def _muxmode(self, linux_pin, mode):
        cmd = 'echo %s > /sys/kernel/debug/gpio_debug/gpio%d/current_pinmux' % (mode, linux_pin)
        self._exec_cmd(self._muxmode.__name__, cmd)

    def _set_drive(self, linux_pin, drive):
        if not self.has_pinmux():
            cmd = 'echo %s > /sys/class/gpio/gpio%d/drive > /dev/null' % (drive, linux_pin)
            self._exec_cmd(self._set_drive.__name__, cmd)

    def _export_pwm(self, channel):
        self.exported_pwm.append(channel)
        cmd = 'echo %d > /sys/class/pwm/pwmchip0/export 2>&1' % channel
        self._exec_cmd(self._export_pwm.__name__, cmd)

    def _unexport_pwm(self, channel):
        cmd = 'echo %d > /sys/class/pwm/pwmchip0/unexport 2>&1' % channel
        self._exec_cmd(self._unexport_pwm.__name__, cmd)

    def _set_pwm_duty_cycle(self, channel, duty_cycle):
        cmd = 'echo %d > /sys/class/pwm/pwmchip0/pwm%d/duty_cycle' % (duty_cycle, channel)
        self._exec_cmd(self._set_pwm_duty_cycle.__name__, cmd)

    def _enable_pwm(self, pwm):
        self.enabled_pwm[pwm] = True
        cmd = 'echo 1 > /sys/class/pwm/pwmchip0/pwm%d/enable' % pwm
        self._exec_cmd(self._enable_pwm.__name__, cmd)

    def __debug(self, func_name, cmd):
        if self.debug:
            now = datetime.datetime.now().strftime("%B %d %I:%M:%S")
            print '{0} {1: <20}{2}'.format(now, func_name + ':', cmd)

    def _exec_cmd(self, caller, command):
        self.__debug(caller, command)
        os.system(command)


setattr(GPIOBase, 'INPUT', INPUT)
setattr(GPIOBase, 'INPUT_PULLUP', INPUT_PULLUP)
setattr(GPIOBase, 'INPUT_PULLDOWN', INPUT_PULLDOWN)
setattr(GPIOBase, 'OUTPUT', OUTPUT)
setattr(GPIOBase, 'ANALOG_INPUT', ANALOG_INPUT)
setattr(GPIOBase, 'PWM', PWM)
setattr(GPIOBase, 'LOW', LOW)
setattr(GPIOBase, 'HIGH', HIGH)


class GPIOGalileo(GPIOBase):

    """Class for managing GPIO pinout on Intel® Galileo board

    See docs/ directory for more information.
    """

    GPIO_MAPPING = {
        0: 50,
        1: 51,
        2: 32,
        3: 18,
        4: 28,
        5: 17,
        6: 24,
        7: 27,
        8: 26,
        9: 19,
        10: 16,
        11: 25,
        12: 38,
        13: 39,
        14: 44,
        15: 45,
        16: 46,
        17: 47,
        18: 48,
        19: 49,
    }

    ADC_MAPPING = {
        14: 0,
        15: 1,
        16: 2,
        17: 3,
        18: 4,
        19: 5,
    }

    PWM_MAPPING = {
        3: 3,
        5: 5,
        6: 6,
        9: 1,
        10: 7,
        11: 4,
    }

    GPIO_MUX_OUTPUT = {
        0: ((40, HIGH), ),
        1: ((41, HIGH), ),
        2: ((31, HIGH), ),
        3: ((30, HIGH), ),
        4: (),
        5: (),
        6: (),
        7: (),
        8: (),
        9: (),
        10: ((41, HIGH), ),
        11: ((43, HIGH), ),
        12: ((54, HIGH), ),
        13: ((55, HIGH), ),
        14: ((37, HIGH), ),
        15: ((36, HIGH), ),
        16: ((23, HIGH), ),
        17: ((22, HIGH), ),
        18: ((21, HIGH), (29, HIGH)),
        19: ((20, HIGH), (29, HIGH)),
    }

    GPIO_MUX_INPUT = GPIO_MUX_OUTPUT
    GPIO_MUX_INPUT_PULLUP = GPIO_MUX_OUTPUT
    GPIO_MUX_INPUT_PULLDOWN = GPIO_MUX_OUTPUT

    GPIO_MUX_ANALOG_INPUT = {
        14: ((37, LOW), ),
        15: ((36, LOW), ),
        16: ((23, LOW), ),
        17: ((22, LOW), ),
        18: ((21, LOW), (29, HIGH)),
        19: ((20, LOW), (29, HIGH)),
    }

    GPIO_MUX_PWM = {
        3: ((30, HIGH), ),
        5: (),
        6: (),
        9: (),
        10: ((41, HIGH), ),
        11: ((43, HIGH), ),
    }

    PWM_MIN_PERIOD = 62500
    PWM_MAX_PERIOD = 7999999
    PWM_DEFAULT_PERIOD = 5000000

    def __init__(self, **kwargs):
        self.adc_iio_device = 0
        super(GPIOGalileo, self).__init__(**kwargs)
        self.pwm_periods = {}
        for pwm in self.PWM_MAPPING.keys():
            self.pwm_periods[pwm] = self.PWM_DEFAULT_PERIOD

    def _set_pwm_period(self, pin, period):
        channel = self.PWM_MAPPING[pin]
        self.pwm_periods[pin] = period
        cmd = 'echo %d > /sys/class/pwm/pwmchip0/pwm%d/period' % (period, channel)
        self._exec_cmd(self._set_pwm_period.__name__, cmd)

    def _get_pwm_period(self, pin):
        return self.pwm_periods[pin]

    def _init_pwm(self, pin):
        linux_pin = self.GPIO_MAPPING[pin]
        self._set_drive(linux_pin, DRIVE_STRONG)
        self._set_direction(linux_pin, OUTPUT)
        self._write_value(linux_pin, HIGH)

        pwm = self.PWM_MAPPING[pin]
        self._export_pwm(pwm)
        self.enabled_pwm[pwm] = False
        self._set_pwm_period(pin, self.pwm_periods[pin])
        self._set_pwm_duty_cycle(pwm, 0)


class GPIOGalileoGen2(GPIOBase):

    """Class for managing GPIO pinout on Intel® Galileo Gen2 board

    See docs/ directory for more information.
    """

    GPIO_MAPPING = {
        0: 11,
        1: 12,
        2: 61,
        3: 62,
        4: 6,
        5: 0,
        6: 1,
        7: 38,
        8: 40,
        9: 4,
        10: 10,
        11: 5,
        12: 15,
        13: 7,
        14: 48,
        15: 50,
        16: 52,
        17: 54,
        18: 56,
        19: 58,
    }

    ADC_MAPPING = {
        14: 0,
        15: 1,
        16: 2,
        17: 3,
        18: 4,
        19: 5,
    }

    PWM_MAPPING = {
        3: 1,
        5: 3,
        6: 5,
        9: 7,
        10: 11,
        11: 9,
    }

    GPIO_MUX_OUTPUT = {
        0: ((32, LOW), (33, NONE)),
        1: ((45, LOW), (28, LOW), (29, NONE)),
        2: ((77, LOW), (34, LOW), (35, NONE), (13, NONE)),
        3: ((64, LOW), (76, LOW), (16, LOW), (17, NONE), (14, NONE)),
        4: ((36, LOW), (37, NONE)),
        5: ((66, LOW), (18, LOW), (19, NONE)),
        6: ((68, LOW), (20, LOW), (21, NONE)),
        7: ((39, NONE), ),
        8: ((41, NONE), ),
        9: ((70, LOW), (22, LOW), (23, NONE)),
        10: ((74, LOW), (26, LOW), (27, NONE)),
        11: ((44, LOW), (72, LOW), (24, LOW), (25, NONE)),
        12: ((42, LOW), (43, NONE)),
        13: ((46, LOW), (30, LOW), (31, NONE)),
        14: ((49, NONE), ),
        15: ((51, NONE), ),
        16: ((53, NONE), ),
        17: ((55, NONE), ),
        18: ((78, HIGH), (60, HIGH), (57, NONE)),
        19: ((79, HIGH), (60, HIGH), (59, NONE)),
    }

    GPIO_MUX_INPUT = {
        0: ((32, HIGH), (33, NONE)),
        1: ((45, LOW), (28, HIGH), (29, NONE)),
        2: ((77, LOW), (34, HIGH), (35, NONE), (13, NONE)),
        3: ((64, LOW), (76, LOW), (16, HIGH), (17, NONE), (14, NONE)),
        4: ((36, HIGH), (37, NONE)),
        5: ((66, LOW), (18, HIGH), (19, NONE)),
        6: ((68, LOW), (20, HIGH), (21, NONE)),
        7: ((39, NONE), ),
        8: ((41, NONE), ),
        9: ((70, LOW), (22, HIGH), (23, NONE)),
        10: ((74, LOW), (26, HIGH), (27, NONE)),
        11: ((44, LOW), (72, LOW), (24, HIGH), (25, NONE)),
        12: ((42, HIGH), (43, NONE)),
        13: ((46, LOW), (30, HIGH), (31, NONE)),
        14: ((49, NONE), ),
        15: ((51, NONE), ),
        16: ((53, NONE), ),
        17: ((55, NONE), ),
        18: ((78, HIGH), (60, HIGH), (57, NONE)),
        19: ((79, HIGH), (60, HIGH), (59, NONE)),
    }

    GPIO_MUX_INPUT_PULLUP = {
        0: ((32, HIGH), (33, HIGH)),
        1: ((45, LOW), (28, HIGH), (29, HIGH)),
        2: ((77, LOW), (34, HIGH), (35, HIGH), (13, NONE)),
        3: ((64, LOW), (76, LOW), (16, HIGH), (17, HIGH), (14, NONE)),
        4: ((36, HIGH), (37, HIGH)),
        5: ((66, LOW), (18, HIGH), (19, HIGH)),
        6: ((68, LOW), (20, HIGH), (21, HIGH)),
        7: ((39, HIGH), ),
        8: ((41, HIGH), ),
        9: ((70, LOW), (22, HIGH), (23, HIGH)),
        10: ((74, LOW), (26, HIGH), (27, HIGH)),
        11: ((44, LOW), (72, LOW), (24, HIGH), (25, HIGH)),
        12: ((42, HIGH), (43, HIGH)),
        13: ((46, LOW), (30, HIGH), (31, HIGH)),
        14: ((49, HIGH), ),
        15: ((51, HIGH), ),
        16: ((53, HIGH), ),
        17: ((55, HIGH), ),
        18: ((78, HIGH), (60, HIGH), (57, HIGH)),
        19: ((79, HIGH), (60, HIGH), (59, HIGH)),
    }

    GPIO_MUX_INPUT_PULLDOWN = {
        0: ((32, HIGH), ),
        1: ((45, LOW), (28, HIGH), (29, LOW)),
        2: ((77, LOW), (34, HIGH), (35, LOW), (13, NONE)),
        3: ((64, LOW), (76, LOW), (16, HIGH), (17, LOW), (14, NONE)),
        4: ((36, HIGH), (37, LOW)),
        5: ((66, LOW), (18, HIGH), (19, LOW)),
        6: ((68, LOW), (20, HIGH), (21, LOW)),
        7: ((39, LOW), ),
        8: ((41, LOW), ),
        9: ((70, LOW), (22, HIGH), (23, LOW)),
        10: ((74, LOW), (26, HIGH), (27, LOW)),
        11: ((44, LOW), (72, LOW), (24, HIGH), (25, LOW)),
        12: ((42, HIGH), (43, LOW)),
        13: ((46, LOW), (30, HIGH), (31, LOW)),
        14: ((49, LOW), ),
        15: ((51, LOW), ),
        16: ((53, LOW), ),
        17: ((55, LOW), ),
        18: ((78, HIGH), (60, HIGH), (57, LOW)),
        19: ((79, HIGH), (60, HIGH), (59, LOW)),
    }

    GPIO_MUX_ANALOG_INPUT = {
        14: ((48, NONE), (49, NONE)),
        15: ((50, NONE), (51, NONE)),
        16: ((52, NONE), (53, NONE)),
        17: ((54, NONE), (55, NONE)),
        18: ((78, LOW), (60, HIGH), (56, NONE), (57, NONE)),
        19: ((79, LOW), (60, HIGH), (58, NONE), (59, NONE)),
    }

    GPIO_MUX_PWM = {
        3: ((64, HIGH), (76, LOW), (16, LOW), (17, NONE), (62, NONE)),
        5: ((66, HIGH), (18, LOW), (19, NONE)),
        6: ((68, HIGH), (20, LOW), (21, NONE)),
        9: ((70, HIGH), (22, LOW), (23, NONE)),
        10: ((74, HIGH), (26, LOW), (27, NONE)),
        11: ((72, HIGH), (24, LOW), (25, NONE)),
    }

    PWM_MIN_PERIOD = 666666
    PWM_MAX_PERIOD = 41666666
    PWM_DEFAULT_PERIOD = 5000000

    def __init__(self, **kwargs):
        self.adc_iio_device = 0
        super(GPIOGalileoGen2, self).__init__(**kwargs)
        self.pwm_period = self.PWM_DEFAULT_PERIOD
        self.is_pwm_period_set = False

    def _set_pwm_period(self, pin, period):
        """On GalileoGen2 all PWM channels share the same period. When this is
        set all the PWM outputs are disabled for at least 1ms while the chip
        reconfigures itself. The PWM pin is then ignored.
        """
        self.pwm_period = period
        cmd = 'echo %d > /sys/class/pwm/pwmchip0/device/pwm_period' % period
        self._exec_cmd(self._set_pwm_period.__name__, cmd)

    def _get_pwm_period(self, pin):
        return self.pwm_period

    def _init_pwm(self, pin):
        pwm = self.PWM_MAPPING[pin]
        self._export_pwm(pwm)
        self._set_pwm_duty_cycle(pwm, 0)
        self.enabled_pwm[pwm] = False
        if not self.is_pwm_period_set:
            self._set_pwm_period(pin, self.pwm_period)
            self.is_pwm_period_set = True


class GPIOEdison(GPIOBase):

    """Class for managing GPIO pinout on Intel®Edison board

    See docs/ directory for more information.
    """

    GPIO_MAPPING = {                                                            
        0: 130,                                                                 
        1: 131,                                                                 
        2: 128,                                                                 
        3:  12,                                                                 
        4: 129,                                                                 
        5:  13,                                                                 
        6: 182,                                                                 
        7:  48,                                                                 
        8:  49,                                                                 
        9: 183,                                                                 
       10:  41,                                                                 
       11:  43,                                                                 
       12:  42,                                                                 
       13:  40,                                                                 
       14:  44,                                                                 
       15:  45,                                                                 
       16:  46,                                                                 
       17:  47,                                                                 
       18:  14,                                                                 
       19: 165,                                                                 
    } 

    ADC_MAPPING = {
        14: 0,
        15: 1,
        16: 2,
        17: 3,
        18: 4,
        19: 5,
    }

    PWM_MAPPING = {
        3: 0,
        5: 1,
        6: 2,
        9: 3,
        # TODO: enable swizzler
        10: None,
        11: None,
    }

    GPIO_MUX_OUTPUT = {
        0:  ((130, MODE_0), (248, HIGH), (216, HIGH)),
        1:  ((131, MODE_0), (249, HIGH), (217, HIGH)),
        2:  ((128, MODE_0), (250, HIGH), (218, HIGH)),
        3:  (( 12, MODE_0), (251, HIGH), (219, HIGH)),
        4:  ((129, MODE_0), (252, HIGH), (220, HIGH)),
        5:  (( 13, MODE_0), (253, HIGH), (221, HIGH)),
        6:  ((182, MODE_0), (254, HIGH), (222, HIGH)),
        7:  (( 48, MODE_0), (255, HIGH), (223, HIGH)),
        8:  (( 49, MODE_0), (256, HIGH), (224, HIGH)),
        9:  ((183, MODE_0), (257, HIGH), (225, HIGH)),
        10: (( 41, MODE_0), (258, HIGH), (226, HIGH), (240, LOW), (263, HIGH)),
        11: (( 43, MODE_0), (259, HIGH), (227, HIGH), (241, LOW), (262, HIGH)),
        12: (( 42, MODE_0), (260, HIGH), (228, HIGH), (242, LOW)),
        13: (( 40, MODE_0), (261, HIGH), (229, HIGH), (243, LOW)),
        14: (( 44, MODE_0), (232, HIGH), (208, HIGH), (200, LOW)),
        15: (( 45, MODE_0), (233, HIGH), (209, HIGH), (201, LOW)),
        16: (( 46, MODE_0), (234, HIGH), (210, HIGH), (202, LOW)),
        17: (( 47, MODE_0), (235, HIGH), (211, HIGH), (203, LOW)),
        18: (( 14, MODE_0), (236, HIGH), (212, HIGH), (204, LOW)),
        19: ((165, MODE_0), (237, HIGH), (213, HIGH), (205, LOW)),
    }

    GPIO_MUX_INPUT = {
        0:  ((130, MODE_0), (248, LOW), (216, NONE)),
        1:  ((131, MODE_0), (249, LOW), (217, NONE)),
        2:  ((128, MODE_0), (250, LOW), (218, NONE)),
        3:  (( 12, MODE_0), (251, LOW), (219, NONE)),
        4:  ((129, MODE_0), (252, LOW), (220, NONE)),
        5:  (( 13, MODE_0), (253, LOW), (221, NONE)),
        6:  ((182, MODE_0), (254, LOW), (222, NONE)),
        7:  (( 48, MODE_0), (255, LOW), (223, NONE)),
        8:  (( 49, MODE_0), (256, LOW), (224, NONE)),
        9:  ((183, MODE_0), (257, LOW), (225, NONE)),
        10: (( 41, MODE_0), (258, LOW), (226, NONE), (240, LOW), (263, HIGH)),
        11: (( 43, MODE_0), (259, LOW), (227, NONE), (241, LOW), (262, HIGH)),
        12: (( 42, MODE_0), (260, LOW), (228, NONE), (242, LOW)),
        13: (( 40, MODE_0), (261, LOW), (229, NONE), (243, LOW)),
        14: (( 44, MODE_0), (232, LOW), (208, NONE), (200, LOW)),
        15: (( 45, MODE_0), (233, LOW), (209, NONE), (201, LOW)),
        16: (( 46, MODE_0), (234, LOW), (210, NONE), (202, LOW)),
        17: (( 47, MODE_0), (235, LOW), (211, NONE), (203, LOW)),
        18: (( 14, MODE_0), (236, LOW), (212, NONE), (204, LOW)),
        19: ((165, MODE_0), (237, LOW), (213, NONE), (205, LOW)),
    }

    GPIO_MUX_INPUT_PULLUP = {
        0:  ((130, MODE_0), (248, LOW), (216, HIGH)),
        1:  ((131, MODE_0), (249, LOW), (217, HIGH)),
        2:  ((128, MODE_0), (250, LOW), (218, HIGH)),
        3:  (( 12, MODE_0), (251, LOW), (219, HIGH)),
        4:  ((129, MODE_0), (252, LOW), (220, HIGH)),
        5:  (( 13, MODE_0), (253, LOW), (221, HIGH)),
        6:  ((182, MODE_0), (254, LOW), (222, HIGH)),
        7:  (( 48, MODE_0), (255, LOW), (223, HIGH)),
        8:  (( 49, MODE_0), (256, LOW), (224, HIGH)),
        9:  ((183, MODE_0), (257, LOW), (225, HIGH)),
        10: (( 41, MODE_0), (258, LOW), (226, HIGH), (240, LOW), (263, HIGH)),
        11: (( 43, MODE_0), (259, LOW), (227, HIGH), (241, LOW), (262, HIGH)),
        12: (( 42, MODE_0), (260, LOW), (228, HIGH), (242, LOW)),
        13: (( 40, MODE_0), (261, LOW), (229, HIGH), (243, LOW)),
        14: (( 44, MODE_0), (232, LOW), (208, HIGH), (200, LOW)),
        15: (( 45, MODE_0), (233, LOW), (209, HIGH), (201, LOW)),
        16: (( 46, MODE_0), (234, LOW), (210, HIGH), (202, LOW)),
        17: (( 47, MODE_0), (235, LOW), (211, HIGH), (203, LOW)),
        18: (( 14, MODE_0), (236, LOW), (212, HIGH), (204, LOW)),
        19: ((165, MODE_0), (237, LOW), (213, HIGH), (205, LOW)),
    }

    GPIO_MUX_INPUT_PULLDOWN = {
        0:  ((130, MODE_0), (248, LOW), (216, LOW)),
        1:  ((131, MODE_0), (249, LOW), (217, LOW)),
        2:  ((128, MODE_0), (250, LOW), (218, LOW)),
        3:  (( 12, MODE_0), (251, LOW), (219, LOW)),
        4:  ((129, MODE_0), (252, LOW), (220, LOW)),
        5:  (( 13, MODE_0), (253, LOW), (221, LOW)),
        6:  ((182, MODE_0), (254, LOW), (222, LOW)),
        7:  (( 48, MODE_0), (255, LOW), (223, LOW)),
        8:  (( 49, MODE_0), (256, LOW), (224, LOW)),
        9:  ((183, MODE_0), (257, LOW), (225, LOW)),
        10: (( 41, MODE_0), (258, LOW), (226, LOW), (240, LOW), (263, HIGH)),
        11: (( 43, MODE_0), (259, LOW), (227, LOW), (241, LOW), (262, HIGH)),
        12: (( 42, MODE_0), (260, LOW), (228, LOW), (242, LOW)),
        13: (( 40, MODE_0), (261, LOW), (229, LOW), (243, LOW)),
        14: (( 44, MODE_0), (232, LOW), (208, LOW), (200, LOW)),
        15: (( 45, MODE_0), (233, LOW), (209, LOW), (201, LOW)),
        16: (( 46, MODE_0), (234, LOW), (210, LOW), (202, LOW)),
        17: (( 47, MODE_0), (235, LOW), (211, LOW), (203, LOW)),
        18: (( 14, MODE_0), (236, LOW), (212, LOW), (204, LOW)),
        19: ((165, MODE_0), (237, LOW), (213, LOW), (205, LOW)),
    }

    GPIO_MUX_ANALOG_INPUT = {
        14: (( 44, MODE_0), (200, HIGH), (232, LOW), (208, NONE)),
        15: (( 45, MODE_0), (201, HIGH), (233, LOW), (209, NONE)),
        16: (( 46, MODE_0), (202, HIGH), (234, LOW), (210, NONE)),
        17: (( 47, MODE_0), (203, HIGH), (235, LOW), (211, NONE)),
        18: (( 14, MODE_0), (204, HIGH), (236, LOW), (212, NONE)),
        19: ((165, MODE_0), (205, HIGH), (237, LOW), (213, NONE)),
    }

    GPIO_MUX_PWM = {
        3:  (( 12, MODE_1), (251, HIGH), (219, NONE)),
        5:  (( 13, MODE_1), (253, HIGH), (221, NONE)),
        6:  ((182, MODE_1), (254, HIGH), (222, NONE)),
        9:  ((183, MODE_1), (257, HIGH), (225, NONE)),
        10: (( 41, MODE_1), (258, HIGH), (226, NONE), (240, LOW), (263, HIGH)),
        11: (( 43, MODE_1), (259, HIGH), (227, NONE), (241, LOW), (262, HIGH)),
    }

    PWM_MIN_PERIOD = 104
    PWM_MAX_PERIOD = 218453000
    PWM_DEFAULT_PERIOD = 2048000

    def __init__(self, **kwargs):
        self.pinmux = 214
        self.adc_iio_device = 1
        super(GPIOEdison, self).__init__(**kwargs)
        self.pwm_periods = {}
        for pin in self.PWM_MAPPING.keys():
            self.pwm_periods[pin] = self.PWM_DEFAULT_PERIOD
        # Set all pins into a safe state at startup.
        for i in range(0, 20):
            self.pinMode(i, INPUT)

    def _set_pwm_period(self, pin, period):
        self.pwm_periods[pin] = period
        channel = self.PWM_MAPPING[pin]
        cmd = 'echo %d > /sys/class/pwm/pwmchip0/pwm%d/period' % (period, channel)
        self._exec_cmd(self._set_pwm_period.__name__, cmd)

    def _get_pwm_period(self, pin):
        return self.pwm_periods[pin]

    def _init_pwm(self, pin):
        pwm = self.PWM_MAPPING[pin]
        self._export_pwm(pwm)
        self._set_pwm_period(pin, self.pwm_periods[pin])
        self._set_pwm_duty_cycle(pwm, 0)
        self._enable_pwm(pwm)
