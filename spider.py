#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
import urlparse

############ UNICODE ##############
# Some useful unicode functions

def decode_string(v, encoding="utf-8"):
    """ Returns the given value as a Unicode string (if possible).
    """
    if isinstance(encoding, basestring):
        encoding = ((encoding,),) + (("windows-1252",), ("utf-8", "ignore"))
    if isinstance(v, str):
        for e in encoding:
            try:
                return v.decode(*e)
            except:
                pass
        return v
    return unicode(v)

def encode_string(v, encoding="utf-8"):
    """ Returns the given value as a Python byte string (if possible).
    """
    if isinstance(encoding, basestring):
        encoding = ((encoding,),) + (("windows-1252",), ("utf-8", "ignore"))
    if isinstance(v, unicode):
        for e in encoding:
            try:
                return v.encode(*e)
            except:
                pass
        return v
    return str(v)

u = decode_utf8 = decode_string
s = encode_utf8 = encode_string

# For clearer source code:
bytestring = s

############## A simple crawler#####################


class Link(object):

    def __init__(self, url, text="", relation="", referrer=""):
        """ A hyperlink parsed from a HTML document, in the form:
            <a href="url"", title="text", rel="relation">xxx</a>.
        """
        self.url, self.text, self.relation, self.referrer = \
            u(url), u(text), u(relation), u(referrer),

    @property               # generate read-only properties
    def description(self):  # target description
        return self.text

    # Used for sorting the links for crawler queue
    # eq - equal, and so on
    def __eq__(self, link):
        return self.url == link.url

    def __ne__(self, link):
        return self.url != link.url

    def __lt__(self, link):
        return self.url < link.url

    def __gt__(self, link):
        return self.url > link.url


class HTMLLinkParser(HTMLParser):
    '''
    Custom HTML linkparser
    '''

    def __init__(self):
        HTMLParser.__init(self)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def unknown_starttag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def unknown_endtag(self, tag):
        self.handle_endtag(tag)

    def clean(html):
        html = decode_utf8(html)
        html = html.replace("<!", "&lt;!")
        html = html.replace("&lt;!DOCTYPE", "<!DOCTYPE")
        html = html.replace("&lt;!doctype", "<!doctype")
        html = html.replace("&lt;!--", "<!--")
        return html


def base(url):
    """ Returns the URL domain name:
    """
    return urlparse.urlparse(url).netloc


def check_url(url):
    """
    This function verifies that the given 'url' is well formatted,
    this means that it has defined a protocol and a domain.
    The urlparse.urlparse() function is used.

    The return values can be 'True'/'False'.
    """
    try:
        url_parsed = urlparse.urlparse(url)
        if url_parsed.scheme and url_parsed.netloc:
            return True
        else:
            return False

    except Exception as e:
        print '[!] Exception in check_url() function'
        print type(e)     # the exception instance
        print e.args      # arguments stored in .args
        print e           # __str__ allows args to printed directly
        return -1

# Crawling parameters
DEPTH = "depth"
BREADTH = "breadth"
