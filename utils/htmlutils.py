#!/usr/bin/env python
#
# htmlutils.py
#
#  Copyright (c) 2005  Yusuke Shinyama <yusuke at cs dot nyu dot edu>
#  
#  Permission is hereby granted, free of charge, to any person
#  obtaining a copy of this software and associated documentation
#  files (the "Software"), to deal in the Software without
#  restriction, including without limitation the rights to use,
#  copy, modify, merge, publish, distribute, sublicense, and/or
#  sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following
#  conditions:
#  
#  The above copyright notice and this permission notice shall be
#  included in all copies or substantial portions of the Software.
#  
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
#  KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
#  WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
#  PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
#  COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#  SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import re, sys, codecs
from urllib import unquote

stderr = sys.stderr

DEFAULT_CHARSET = 'iso-8859-1'


# english, cyrillic, greek, japanese, chinese
ALPHABET = re.compile(ur'[a-zA-Z0-9\u0390-\u03cf\u0400-\u045f\u3040-\u30ff\u4e00-\u9fff\uff10-\uff19\uff20-\uff9f]')
def get_alphabets(s):
  return ALPHABET.findall(s)

SPACE = re.compile(ur'^\s+$')
def is_space(s):
  return SPACE.match(s)

REMOVE_SPACES = re.compile(ur'\s+')
def remove_spaces(s):
  return REMOVE_SPACES.sub(u' ', s)

def concat(r):
  return remove_spaces(u''.join(r)).strip()


REMOVE_NAME = re.compile(r'#.*$')
def wash_url(url):
  return REMOVE_NAME.sub('', url.strip().encode('ascii', 'replace'))


# encode_element
KEY_ATTRS = dict.fromkeys('id class align valign rowspan colspan'.split(' '))
def encode_element(e):
  return e.tag + ''.join(sorted( ':%s=%s' % (k.lower(), e.attrs[k].lower())
                                 for k in e.attrs.keys() if k in KEY_ATTRS ))


# html tags

BLOCK = dict.fromkeys(
  "head title body p h1 h2 h3 h4 h5 h6 tr td th dt dd li "
  "ul ol dir menu pre dl div center frameset "
  "blockquote table fieldset address".split(" "))

CDATA = dict.fromkeys('script style'.split(' '))

INLINE = dict.fromkeys(
  "comment tt i b u s strike big small nobr em strong dfn code samp kbd var cite abbr "
  "acronym a applet object button font map q sub sup span bdo layer ilayer iframe "
  "select textarea label button option".split(" "))

INLINE_IMMED = dict.fromkeys(
  "basefont br area link img param hr input "
  "colgroup col frame isindex meta base embed".split(" "))

NON_NESTED = dict.fromkeys("form noembed noframes noscript nolayer".split(" "))

VALID_TAGS = {}
for d in (BLOCK, CDATA, INLINE, INLINE_IMMED, NON_NESTED):
  for t in d.iterkeys():
    assert t not in VALID_TAGS, t
    VALID_TAGS[t] = 1
    

# mappings from html charsets to python codecs.
ALT_CODECS = {
  "x-euc-jp": "euc-jp",
  "x-sjis": "ms932",
  "shift-jis": "ms932",
  "shift_jis": "ms932",
  "sjis": "ms932",
}

# getcodec
def getcodec(charset, default=DEFAULT_CHARSET):
  if charset in ALT_CODECS:
    charset = ALT_CODECS[charset]
  if not charset:
    charset = default
  try:
    codecs.lookup(charset)
    return charset
  except LookupError:
    return default

QUOTEREFS = { '&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;' }
# quotestr(s, codec)
def quotestr(s, codec="ascii", quote_special=True):
    """Convert special characters in the string s into proper entitierefs
    with the given codec. The return value must be raw (non-Unicode) string."""
    def quote1(c):
        if quote_special and c in QUOTEREFS:
        return QUOTEREFS[c]
        else:
            return c.encode(codec, 'xmlcharrefreplace')
            return ''.join( quote1(c) for c in s )

# attr2str
def attr2str(attrseq):
    r = []
    for (k,v) in attrseq:
    if v == None:
      r.append(' '+quotestr(k))
    else:
      r.append(' %s="%s"' % (quotestr(k), quotestr(v)))
    return ''.join(r)

# urldecode(s)
ARGPAT = re.compile(r'([^=]+)=(.*)')
def urldecode(s):
    """Convert a query string s into a mapping type.
    Duplicated arguments are not supported.
    Each parameter must occur at most only once."""
    args = {}
    for arg1 in s.split("&"):
        m = ARGPAT.match(arg1)
        if m:
            args[unquote(m.group(1))] = unquote(m.group(2))
    return args