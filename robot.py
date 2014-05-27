#!/usr/bin/env python2
# -*- coding: utf-8 -*-

## Note:  this requires the python bindings for selenium and pyphantomjs if you want to use it

import sys
import time
import string
import re
from urlparse import urlparse
import getopt
import lxml.html
from lxml import etree

from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait

#***************************** BUILD your browser here************************************
DRIVER = ["firefox", "chrome", "phantomjs"]


class Browser(object):
    """
    * This takes care of building a browser based on user preferences'and define its actions
    * crawlwait defines the implicit time wait after firing an event
    * crawlreload defines the tme wait after loading a URL
    """

    def __init__(self, driver, crawlwait=2, crawlreload=):
        self.driver = driver   # Can be DRIVER[i]
        self.crawlwait = crawlwait
        self. crawlreload = crawlreload

    def browserBuilder(self, driver):
        """
        * create a browser based on WebDriverWait
        """
        # handle each case
        if driver == "firefox":
            profile = FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", "127.0.0.1")
            profile.set_preference("network.proxy.http_port", "8008")
            #use proxy for everything, including localhost
            profile.setPreference("network.proxy.no_proxies_on", "");
            profile.update_preferences()
            browser = Firefox(firefox_profile=profile)

            return browser

        elif driver == "chrome":
            options = ChromeOptions()
            # set proxy options
            optionsChrome.addArguments("--proxy-server=http://127.0.0.1:8008/")
            browser = ChromeDriver(optionsChrome)

            return browser

        elif driver == "phantomjs":
            #proxy configuration
            service_args = [
                            '--proxy=127.0.0.1:8008',
                            '--proxy-type=http',
            ]
            browser = PhantomJS('../path_to/phantomjs', service_args=service_args)

            return browser

    def goToURL(self, url):
        """
        * For now, only valid URLs supported

        # TODO: add exception checking for invalid URLs
        """
        try:
            #navigate().to() and get() are synonyms :)
            browser.get(url)
            handlePopUps()
        except WebDriverException, e:
            pass   
        else InterruptedException, e:
            print "goToUrl got interrupted while waiting for the page to be loaded ", e
            pass        
    
    def handlePopUps():
        try:
            # Execute JS
            browser.execute_script("window.alert = function(msg){return true;};" \
                    + "window.confirm = function(msg){return true;};" \
                    + "window.prompt = function(msg){return true;};" \
                )
        except UnexpectedAlertPresentException, e:
            print "Unexpected Alert element: ", e
            pass

    def fireEventWait():
        """
        * Fires the event and waits for a specified time. 
        * webElement: is the element to fire event on.
        * eventable: The HTML event type (onclick, onmouseover, ...).
        * This will return true if firing event is successful.
        * else throws an InterruptedException when interrupted during the wait.
        """
        try:
            element.click()
        except ElementNotVisibleException, e:
            print "Element not present: ", e
            pass

    def screenshot(browser, file):
        """
        * Takes screenshot of current page
        * Only some webdrivers support it
        """
        try:
            print "Taking screenshot: %s" % filename
            browser.save_screenshot(filename)
        except Exception, e:
            print "Error: ", e

    def goback():
        """
        * Gives the back navigation
        * Not very accurate, could possibly result in error
        """
        try:
            browser.back()
        except:
            pass

    def close():
        # * Closes the browser instance
        print "Closing the browser instance..."
        browser.quit()


#******************************************************************************************
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

    * Right now, only support `click` event.
    * The elements would be identified by the name, id, xpath.
    """

    def __init__(self, event, element):
        self.event = 'click' # hardcoded for right now
        self.element = element