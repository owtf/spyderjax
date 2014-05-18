#!/usr/bin/env python2
# -*- coding: utf-8 -*-

# Build browser
# 
import sys
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait, select
import time


######******* BUILD your browser here************
# Comment out the webdriver which will not be used
profile = FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.http", "127.0.0.1")
profile.set_preference("network.proxy.http_port", "8008")
profile.update_preferences()

driver = Firefox(firefox_profile=profile)
#driver = Chromedriver(<pathtoexecutable>)

# OR could do this by defining it in a function
'''
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile

def get_profile():
    # get the Firefox profile object
    firefoxProfile = FirefoxProfile()
    firefoxProfile.set_preference(<>)
    return firefoxProfile

driver = Firefox(firefox_profile=firefoxProfile)
'''
#************************************************

class spider():
    """
    * A robot which clicks the clickable elements in DOM, and captures page snapshots for each
    state change until there are no more available.

    * It fires all possible events on a candidate element.

    * 
    """
    # crawl depth (0 implies infinite)
    def __init__(self, base_url, depth=0, state, snapshot=None):
        self.base_url = target
        self.depth = depth
        self.state = state
        self.snapshot = snapshot


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

    def wait(self, timeout=2.5):
        """
        Explicit timeout for the `webdriver`
        """
        WebDriverWait(self, timeout)


    