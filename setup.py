# -*- coding: utf-8 -*-
#
# Copyright © 2014, Emutex Ltd.
# All rights reserved.
# http://www.emutex.com
#
# Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>
#
# See license in LICENSE.txt file.


from distutils.core import setup

setup(
    name='Wiring-x86',
    version='1.0.0',
    author='Nicolás Pernas Maradei',
    author_email='nicolas.pernas.maradei@emutex.com',
    url='https://github.com/emutex/wiring-x86',
    py_modules=['wiringx86'],
    license='BSD',
    description='A Python module to use most Arduino wiring functions on Intel® Arduino capable boards.',
    long_description=open('README.rst').read(),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
