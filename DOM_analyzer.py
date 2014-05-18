#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
from lxml import html


# Get HTML page from the robot, then analyze for clickable elements, 
# and fire/trigger specific events on them.

# Initialize parser
parser = html.HTMLParser(encoding='unicode', remove_blank_text=True, remove_comments=True, remove_pis=True)


def get_strippedDOM(html):
    """
 * An interface that can be used to strip DOMs. The input and output of a no not have to be valid DOMs.
 * Note that browser interaction is always done on the original DOM, not the modified dom return by a stripper.
 * This will strip the DOM (html source) of any whitespace, comments, any badly formatted attributes  
    
    """
  # REGEX