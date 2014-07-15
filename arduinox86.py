# -*- coding: utf-8 -*-

#########################################################################
# Copyright © 2014, Emutex Ltd.
# All rights reserved.
# http://www.emutex.com
#
# Author: Nicolás Pernas Maradei <nicolas.pernas.maradei@emutex.com>
# Author: Dave Hunt <dave@emutex.com>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# 3. All modifications to the source code must be clearly marked as
#    such. Binary redistributions based on modified source code must
#    be clearly marked as modified versions in the documentation and/or
#    other materials provided with the distribution.
#
# 4. The name of Emutex Ltd. may not be used to endorse or promote
#    products derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
#########################################################################

INPUT = 'in'
INPUT_PULLUP = 'in_pullup'
INPUT_PULLDOWN = 'in_pulldown'
OUTPUT = 'out'
LOW = 'low'
HIGH = 'high'
NONE = 'in'
DRIVE_STRONG = 'strong'


class GPIOGalileoGen2(object):
    
    GPIO_MAPPING = {
        0: 11,
        1: 12,
        2: 13,
        3: 14,
        4: 6,
        5: 0,
        6: 1,
        7: 2,
        8: 3,
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

    GPIO_MUX_OUTPUT = {
        0: ( (32, LOW), (33, NONE) ),
        1: ( (45, LOW), (28, LOW), (29, NONE) ),
        2: ( (77, LOW), (34, LOW), (35, NONE) ),
        3: ( (64, LOW), (76, LOW), (16, LOW), (17, NONE) ),
        4: ( (36, LOW), (37, NONE) ),
        5: ( (66, LOW), (18, LOW), (19, NONE) ),
        6: ( (68, LOW), (20, LOW), (21, NONE) ),
        7: ( (38, LOW), (39, NONE) ), #TODO update for Fab-G
        8: ( (40, LOW), (41, NONE) ), #TODO update for Fab-G
        9: ( (70, LOW), (22, LOW), (23, NONE) ), 
       10: ( (74, LOW), (26, LOW), (27, NONE) ),
       11: ( (44, LOW), (72, LOW), (24, LOW), (25, NONE) ),
       12: ( (42, LOW), (43, NONE) ),
       13: ( (46, LOW), (30, LOW), (31, NONE) ),
       14: ( (49, NONE) ), #FIXME
       15: ( (51, NONE) ), #FIXME
       16: ( (53, NONE) ), #FIXME
       17: ( (55, NONE) ), #FIXME
       18: ( (78, HIGH), (60, HIGH), (57, NONE) ),
       19: ( (79, HIGH), (60, HIGH), (59, LOW) ),
    }

