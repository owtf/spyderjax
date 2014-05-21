#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import os
import re
import lxml.html

from lib.htmlmin import *

"""
class Eventable(object):
    """
    # Events common to elements given below
    GLOBAL_EVENTS = ['onclick', 'ondblclick', 'onmousedown', 'onmousemove', 
            'onmouseout', 'onmouseover', 'onmouseup']

    # Special events for each element.
    EVENTS_PER_ELEMENT = {
            'body': ['onload'],
            'form': ['onsubmit', 'onreset'],
            'input' : ['onselect', 'onchange', 'onfocus', 'onblur','onkeydown', 'onkeypress', 'onkeyup'],
            'textarea': ['onselect', 'onchange', 'onfocus', 'onblur', 'onkeydown', 'onkeypress', 'onkeyup'],
            'select': ['onchange', 'onfocus', 'onblur'],
            'button': ['onfocus', 'onblur'],
            'label': ['onfocus', 'onblur']
    }

    * Eventable class: an element having an event attached to it (onclick, onmouseover, ...) so that it
    * can change the DOM state.
    """ 
"""



class ProcessDOM(object):

    def __init__(self, html, url):
    """
    * Get HTML page from the robot, then analyze for clickable elements, 
    * and fire/trigger specific events on them.
    """
        self.html = html
        self.url = url


    def parse(self):
        """
        * This will convert the html source into a dom object
        * Note that browser interaction is always done on the original DOM, not the modified dom.
        """
        # Convert html source to dom object
        dom = lxml.html.tostring(self.html)
        dom.make_links_absolute(self.url)
        return dom


    def levenshtein(string1, string2):
        """ 
        * Measures the amount of difference between two strings.
        * The return value is the number of operations (insert, delete, replace)
          required to transform string a into string b.

        * This will be used to compare DOM states

        """
        # http://hetland.org/coding/python/levenshtein.py
        n, m = len(string1), len(string2)
        if n > m: 
            # Make sure n <= m to use O(min(n,m)) space.
            string1, string2, n, m = string2, string1, m, n
        current = range(n+1)
        for i in xrange(1, m+1):
            previous, current = current, [i]+[0]*n
            for j in xrange(1, n+1):
                insert, delete, replace = previous[j]+1, current[j-1]+1, previous[j-1]
                if string1[j-1] != string2[i-1]:
                    replace += 1
                current[j] = min(insert, delete, replace)
        return current[n]
