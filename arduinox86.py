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
       19: ( (79, HIGH), (60, HIGH), (59, NONE) ),
    }

    GPIO_MUX_INPUT = {
        0: ( (32, HIGH), (33, NONE) ),
        1: ( (45, LOW), (28, HIGH), (29, NONE) ),
        2: ( (77, LOW), (34, HIGH), (35, NONE) ),
        3: ( (64, LOW), (76, LOW), (16, HIGH), (17, NONE) ),
        4: ( (36, HIGH), (37, NONE) ),
        5: ( (66, LOW), (18, HIGH), (19, NONE) ),
        6: ( (68, LOW), (20, HIGH), (21, NONE) ),
        7: ( (38, HIGH), (39, NONE) ), #TODO update for Fab-G
        8: ( (40, HIGH), (41, NONE) ), #TODO update for Fab-G
        9: ( (70, LOW), (22, HIGH), (23, NONE) ),
       10: ( (74, LOW), (26, HIGH), (27, NONE) ),
       11: ( (44, LOW), (72, LOW), (24, HIGH), (25, NONE) ),
       12: ( (42, HIGH), (43, NONE) ),
       13: ( (46, LOW), (30, HIGH), (31, NONE) ),
       14: ( (49, NONE) ), #FIXME
       15: ( (51, NONE) ), #FIXME
       16: ( (53, NONE) ), #FIXME
       17: ( (55, NONE) ), #FIXME
       18: ( (78, HIGH), (60, HIGH), (57, NONE) ),
       19: ( (79, HIGH), (60, HIGH), (59, NONE) ),
    }

    GPIO_MUX_INPUT_PULLUP = {
        0: ( (32, HIGH), (33, HIGH) ),
        1: ( (45, LOW), (28, HIGH), (29, HIGH) ),
        2: ( (77, LOW), (34, HIGH), (35, HIGH) ),
        3: ( (64, LOW), (76, LOW), (16, HIGH), (17, HIGH) ),
        4: ( (36, HIGH), (37, HIGH) ),
        5: ( (66, LOW), (18, HIGH), (19, HIGH) ),
        6: ( (68, LOW), (20, HIGH), (21, HIGH) ),
        7: ( (38, HIGH), (39, HIGH) ), #TODO update for Fab-G
        8: ( (40, HIGH), (41, HIGH) ), #TODO update for Fab-G
        9: ( (70, LOW), (22, HIGH), (23, HIGH) ),
       10: ( (74, LOW), (26, HIGH), (27, HIGH) ),
       11: ( (44, LOW), (72, LOW), (24, HIGH), (25, HIGH) ),
       12: ( (42, HIGH), (43, HIGH) ),
       13: ( (46, LOW), (30, HIGH), (31, HIGH) ),
       14: ( (49, HIGH) ), #FIXME
       15: ( (51, HIGH) ), #FIXME
       16: ( (53, HIGH) ), #FIXME
       17: ( (55, HIGH) ), #FIXME
       18: ( (78, HIGH), (60, HIGH), (57, HIGH) ),
       19: ( (79, HIGH), (60, HIGH), (59, HIGH) ),
    }

    GPIO_MUX_INPUT_PULLDOWN = {
        0: ( (32, HIGH) ),
        1: ( (45, LOW), (28, HIGH), (29, LOW) ),
        2: ( (77, LOW), (34, HIGH), (35, LOW) ),
        3: ( (64, LOW), (76, LOW), (16, HIGH), (17, LOW) ),
        4: ( (36, HIGH), (37, LOW) ),
        5: ( (66, LOW), (18, HIGH), (19, LOW) ),
        6: ( (68, LOW), (20, HIGH), (21, LOW) ),
        7: ( (38, HIGH), (39, LOW) ), #TODO update for Fab-G
        8: ( (40, HIGH), (41, LOW) ), #TODO update for Fab-G
        9: ( (70, LOW), (22, HIGH), (23, LOW) ),
       10: ( (74, LOW), (26, HIGH), (27, LOW) ),
       11: ( (44, LOW), (72, LOW), (24, HIGH), (25, LOW) ),
       12: ( (42, HIGH), (43, LOW) ),
       13: ( (46, LOW), (30, HIGH), (31, LOW) ),
       14: ( (49, LOW) ), #FIXME
       15: ( (51, LOW) ), #FIXME
       16: ( (53, LOW) ), #FIXME
       17: ( (55, LOW) ), #FIXME
       18: ( (78, HIGH), (60, HIGH), (57, LOW) ),
       19: ( (79, HIGH), (60, HIGH), (59, LOW) ),
    }
