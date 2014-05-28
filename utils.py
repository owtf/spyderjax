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
import lxml.html
import lxml.etree
import hashlib

from lxml.html.clean import Cleaner


class ProcessDOM(object):
    """
    * Get HTML page from the robot, then analyze for clickable elements, 
    * and fire/trigger specific events on them.
    """
    def __init__(self, html, url, browser, tree):
        self.html = html
        self.url = url
        self.tree = self.parse()

    def getStrippedDOM(self):
        """
        Clean HTML using lxml.html.clean.Cleaner
        """
        cleaner = Cleaner(comments=True, javascript=True,
        scripts=True, safe_attrs_only=True, page_structure=True,
        style=True)

        return cleaner.clean_html(self.html)

    def parse(self):
        """
        * This will convert the html source into a dom object
        * Note that browser interaction is always done on the original DOM, not the modified dom.
        """
        parser = lxml.etree.HTMLParser()
        # Convert html source to dom object
        # Error catching because of badly formatted HTML, although lxml tends to perform very well :)
        try:
            tree = lxml.etree.fromstring(self.html.getStrippedDOM(), parser).getroottree() # Returns a XML tree
            page = tree.getroot()
            return tree
        except:
            print "Error in parsing HTML.."
            # What to do here?
        # This will almost certainly not work here
        # make_links_absolute(url)

    def getElementById(self, element, Id):
        """return the first element with this id attribute.
        Return None if not available
        >>> from lxml.etree import tostring,fromstring,Element,SubElement
        >>> s = '<div><p id="myId">Some text</p></div>'
        >>> elt = fromstring(s)
        >>> e = getElementById(elt,'myId')
        >>> tostring(e)
        '<p id="myId">Some text</p>'
        >>> e = getElementById(elt,'anotherId')
        >>> e is None
        True
        """
        try:
            return element.xpath("//*[@id='%s']" % (Id,))[0]
        except IndexError:
            return None

    def xpath(self, expression):
        return self.tree.xpath(expression)
  
    def css_select(self, expression, text = False):
        from lxml.cssselect import CSSSelector
        sel = CSSSelector(expression)
        selected_elements = sel(self.tree)
        if text:
            selected_elements = map(lambda x: x.text, selected_elements)
        return selected_elements

    def hashcode(self):
        """
        * Calculates a hash based on html string
        """
        string = lxml.html.fromstring(self.html).tostring()
        return hashlib.md5(string).hexdigest

    def levenshtein(string1, string2):
        """ 
        * Measures the amount of difference between two strings.
        * The return value is the number of operations (insert, delete, replace)
          required to transform string a into string b.

        * This will be used to compare DOM states
        * The edit distance algorithm.

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


#*************************************************************************************************
#thanks to Mark Pilgrim for these lists 
#http://feedparser.org/docs/html-sanitization.html

allowed_tags = set(('a', 'abbr', 'acronym', 'address', 'area', 'b', 'big',
'blockquote', 'br', 'button', 'caption', 'center', 'cite', 'code', 'col',
'colgroup', 'dd', 'del', 'dfn', 'dir', 'div', 'dl', 'dt', 'em', 'fieldset',
'font', 'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
'input', 'ins', 'kbd', 'label', 'legend', 'li', 'map', 'menu', 'ol',
'optgroup', 'option', 'p', 'pre', 'q', 's', 'samp', 'select', 'small',
'span', 'strike', 'strong', 'sub', 'sup', 'table', 'tbody', 'td',
'textarea', 'tfoot', 'th', 'thead', 'tr', 'tt', 'u', 'ul', 'var'))
  
allowed_attributes = set(('abbr', 'accept', 'accept-charset', 'accesskey',
'action','align', 'alt', 'axis', 'border', 'cellpadding', 'cellspacing',
'char','charoff', 'charset', 'checked', 'cite', 'class', 'clear', 'cols',
'colspan', 'color', 'compact', 'coords', 'datetime', 'dir', 'disabled',
'enctype', 'for', 'frame', 'headers', 'height', 'href', 'hreflang',
'hspace', 'id', 'ismap', 'label', 'lang', 'longdesc', 'maxlength',
'media', 'method', 'multiple', 'name', 'nohref', 'noshade', 'nowrap',
'prompt', 'readonly', 'rel', 'rev', 'rows', 'rowspan', 'rules',
'scope', 'selected', 'shape', 'size', 'span', 'src', 'start',
'summary', 'tabindex', 'target', 'title', 'type', 'usemap', 'valign',
'value', 'vspace', 'width'))
