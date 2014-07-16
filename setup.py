# -*- coding: utf-8 -*-
"""
 Copyright © 2014, Emutex Ltd.
 All rights reserved.
 http://www.emutex.com

 Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>

 Redistribution and use in source and binary forms, with or without
 modification, are permitted provided that the following conditions
 are met:

 1. Redistributions of source code must retain the above copyright
    notice, this list of conditions and the following disclaimer.

 2. Redistributions in binary form must reproduce the above copyright
    notice, this list of conditions and the following disclaimer in
    the documentation and/or other materials provided with the
    distribution.

 3. All modifications to the source code must be clearly marked as
    such. Binary redistributions based on modified source code must
    be clearly marked as modified versions in the documentation and/or
    other materials provided with the distribution.

 4. The name of Emutex Ltd. may not be used to endorse or promote
    products derived from this software without specific prior written
    permission.

 THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
 "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
 LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
 FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
 COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
 INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES INCLUDING,
 BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
 LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
 CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
 LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
 ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
 POSSIBILITY OF SUCH DAMAGE.
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
