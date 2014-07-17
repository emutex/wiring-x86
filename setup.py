# -*- coding: utf-8 -*-
"""
 Copyright © 2014, Emutex Ltd.
 All rights reserved.
 http://www.emutex.com

 Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>

 See license in LICENSE file.
"""

from distutils.core import setup

setup(
    name='Arduinox86',
    version='0.1',
    author='Nicolás Pernas Maradei',
    author_email='nicolas.pernas.maradei@emutex.com',
    #     url='',
    py_modules=['arduinox86'],
    license='BSD',
    description='A Python module to use basic GPIO on Intel® Arduino capable boards.',
    long_description=open('README.md').read(),
    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
)
