#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
owtf is an OWASP+PTES-focused try to unite great tools and facilitate pen testing
Copyright (c) 2011, Abraham Aranguren <name.surname@gmail.com> Twitter: @7a_ http://7-a.org
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the copyright owner nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
from datetime import datetime
import random
import string

from six import u

def generate_timestamped_string(subject="test", number_of_random_chars=4):
    """
    Generate time-stamped string. Format as follows...

    `2013-01-31_14:12:23_SubjectString_a3Zg`


    Kwargs:
        subject (str): String to use as subject.
        number_of_random_chars (int) : Number of random characters to append.

    + This method is helpful for creating unique names with timestamps in them
    """
    random_str = generate_random_string(number_of_random_chars)
    timestamp = generate_timestamp()
    return u"{timestamp}_{subject}_{random_str}".format(timestamp=timestamp,
                                                        subject=subject,
                                                        random_str=random_str)

def generate_timestamp(date_format="%Y-%m-%d_%H.%M.%S"):
    """
    Returns timestamped string. '2012-03-15_14:42:23

    Kwargs:
        format: A date/time format string.  If not specified, the default will be used.

    """
    return datetime.now().strftime(date_format)


def generate_random_string(number_of_random_chars=8, character_set=string.ascii_letters):
    """
    Generate a series of random characters.

    Kwargs:
        number_of_random_chars (int) : Number of characters long
        character_set (str): Specify a character set.  Default is ASCII
    """
    return u('').join(random.choice(character_set)
                      for _ in range(number_of_random_chars))
