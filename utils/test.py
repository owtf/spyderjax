#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
import random
import string

from six import u

from operator import itemgetter
from __future__ import generators


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
    return "{timestamp}_{subject}_{random_str}".format(timestamp=timestamp,
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
