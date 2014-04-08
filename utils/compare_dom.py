#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import hashlib


class CheckDOM():
    '''
    Check for DOM changes after clicking clickable elements
    '''

    def __init__(self, html):
        self.html = html

    def hash(self):
        hashed = hashlib.md5(self.html)
        return str(hashed)
