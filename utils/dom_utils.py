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
import hashlib
import re
import sys

from lxml import html
from lxml.html.clean import Cleaner
from lxml.cssselect import CSSSelector

from urlparse import urlparse
from robot import Browser


def normalize(html):
    """Normalize the input HTML using lxml.html.clean.Cleaner
    """
    cleaner = Cleaner(comments=True, javascript=True,
        scripts=True, safe_attrs_only=True, page_structure=True,
        style=True)

    return cleaner.clean_html(html)

# DOM equivalence algorithm
def isequivalent(dom1, dom2):

    hash1 = hashcode(normalize(dom1))
    hash2 = hashcode(normalize(dom2))

    if hash1 == hash2:
        return True
    else:
        return False

def parse(html):
    """
    + This will convert the html source into a dom object
    + Note that browser interaction is always done on the original DOM, not the modified dom.
    """
    # Convert html source to dom object
    # Error catching because of badly formatted HTML, although lxml tends to perform very well :)
    try:
        tree = html.fromstring(normalize(html))
        return tree
    except:
        print "Error in parsing HTML.."

def xpath(expression):
        return self.tree.xpath(expression)
  
    def css_select(self, expression, text = False):
        sel = CSSSelector(expression)
        selected_elements = sel(self.tree)
        if text:
            selected_elements = map(lambda x: x.text, selected_elements)
        return selected_elements

# Computes a hashcode from string to compare if 2 DOMs are equivalent
def hashcode(string):
    """
    + Calculates a hash based on html string
    """
    return hashlib.md5(string).hexdigest()

# Implemented in crawljax; not too efficient
# It is too uptight on equivalence - would probably lead to state explosion
def levenshtein(string1, string2):
    """
    + Measures the amount of difference between two strings.
    + The return value is the number of operations (insert, delete, replace)
      required to transform string a into string b.
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

def minEditDist(dom1, dom2):
    """
    + Implements the edit-distance method on DOM for backtracking and DOM diff measure
    + Computes the min edit distance from target to source
    + Stolen from http://www.cs.colorado.edu/~martin/csci5832/edit-dist-blurb.html
    """
    n = len(dom1)
    m = len(dom2)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insertCost(dom2[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + deleteCost(dom1[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
           distance[i][j] = min(distance[i-1][j]+1,
                                distance[i][j-1]+1,
                                distance[i-1][j-1]+substCost(dom1[j-1],dom2[i-1]))
    return distance[n][m]

