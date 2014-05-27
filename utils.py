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

import os
import re
import lxml.html


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
        return dom     # This returns a DOM tree


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

    def 