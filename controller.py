#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import urllib2
import config
from lib import htmldom

# Events
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

############ BROWSER CONFIG ###########
robot = config.driver

#######################################

#### Some useful utils ################
def get_unstrippedDOM():
    return robot.page_source


