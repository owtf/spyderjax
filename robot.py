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

* Note:  this requires the python bindings for selenium and pyphantomjs if you want to use it
'''

import sys
import time
import re
import simplejson as json
from lxml import html

from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait


## TODO: Possible optimization in form of passing DOM tree to lxml for analysing and parsing

## Right now, for initial implementation should only include using Selenium to perform DOM tree transversal

#***************************** BUILD your browser here************************************
DRIVER = ["firefox", "chrome", "phantomjs"]


class BrowserBuild(object):
    """
    + This takes care of building a browser based on user preferences'and define its actions
    + crawlwait defines the implicit time wait after firing an event
    + crawlreload defines the tme wait after loading a URL
    """

    def __init__(self, config=None):
        with open('config') as config:
            data = json.load(config)
        self.config = data["browser"]

    def browser(self, driver):
        """
        + create a browser based on WebDriverWait
        """
        # handle each case
        if driver == "firefox":
            profile = FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", "127.0.0.1")
            profile.set_preference("network.proxy.http_port", "8008")
            #use proxy for everything, including localhost
            profile.set_preference("network.proxy.no_proxies_on", "");
            profile.update_preferences()
            browser = Firefox(firefox_profile=profile)

            return browser

        elif driver == "chrome":
            options = ChromeOptions()
            # set proxy options
            options.add_arguments("--proxy-server=http://127.0.0.1:8008/")
            browser = Chrome(executable_path="./chromedriver", options)

            return browser

        elif driver == "phantomjs":
            #proxy configuration
            service_args = (
                            '--proxy=127.0.0.1:8008',\
                            '--proxy-type=http',\
            )
            browser = PhantomJS('../path_to/phantomjs', service_args=service_args)

            return browser


class Browser(object):

    def __init__(self, browser, crawlwait=2, crawlreload=5):
        """
        Instantiates a browser object
        """
        self.browser = browser
        self.crawlwait = crawlwait
        self.crawlreload = crawlreload

    def goToURL(self, url):
        """
        + For now, only valid URLs supported

        # TODO: add exception checking for invalid URLs
        """
        try:
            #navigate().to() and get() are synonyms :)
            self.browser.get(url)
            handlePopUps()
        except WebDriverException, e:
            pass
        except InterruptedException, e:
            print "goToUrl got interrupted while waiting for the page to be loaded ", e
            pass

    def handlePopUps(self):
        try:
            # Execute JS
            self.browser.execute_script("window.alert = function(msg){return true;};" \
                    + "window.confirm = function(msg){return true;};" \
                    + "window.prompt = function(msg){return true;};" \
                )
        except UnexpectedAlertPresentException, e:
            print "Unexpected Alert element: ", e
            pass

    def goback(self):
        """
        + Gives the back navigation
        + Not very accurate, could possibly result in error
        """
        try:
            self.browser.back()
        except:
            pass

    def close(self):
        # * Closes the browser instance
        print "Closing the browser instance..."
        self.browser.quit()

    def screenshotdir(self):
        # http://stackoverflow.com/questions/273192/check-if-a-directory-exists-and-create-it-if-necessary
        directory = 'screenshots'
        if not os.path.exists(directory):
            os.makedirs(directory)

    def screenshot(self, filename):
        """
        + Takes screenshot of current page
        + Only some webdrivers support it

        # Currently not implemented
        """
        try:
            print "Taking screenshot..."
            self.browser.save_screenshot(filename)
        except Exception, e:
            print "Error: ", e

    def getDOM(self):
        return self.browser.page_source


DEFAULT_ELEMENTS = ["a", "button", "li", "nav", "ol", "span", "ul", "header", "footer", "section"]

    def extractPath(self, dom):
        """
        + Method to get clickable elements from browser DOM (using XPath)
        + List of eligible elements will come from config file
        """

        tree = html.fromstring(dom)

        clicable_element_types = tuple('%s[not(contains(@class, "selenium_donotclick"))]' % i for i in (
            'a', 'submit', 'input[@type="submit"]',
        ))
        xpath = '|'.join('//%s' % item for item in clicable_element_types)

    def click(self, element):
        try:
            element.click()
            # wait for AJAX/JS to load completely
            self.browser.implicitly_wait(5) # seconds
        except WebDriverException:
            #  Some element doesn't need to be visible. Maybe some JS was slow
            # so element few ms ago was visible, but not now.
            pass
        except Exception as e:
            pass

