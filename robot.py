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

# This is a part of Google Summer of Code 2014 project, OWASP OWTF
'''
import sys
import time
import re
import simplejson as json
from lxml import html

from urllib2 import urlopen
import urllib2

from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait


## TODO: Possible optimization in form of passing DOM tree to lxml for analysing and parsing

## Right now, for initial implementation should only include using Selenium to perform DOM tree transversal

#***************************** BUILD your browser here************************************
class WebDriverFactory(object):
    """
    This takes care of building a browser based on config file
    """

    def __init__(self, config):
        with open('config.json') as config:
            data = json.load(config)
        self.config = data

    def create_webdriver(self, driver):
        """
        create a browser based on WebDriverWait
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
            browser = Chrome(executable_path=self.config["chromedriver_path"], options)

            return browser

        elif driver == "phantomjs":
            #proxy configuration
            service_args = (
                            '--proxy=127.0.0.1:8008',\
                            '--proxy-type=http',\
                            '--ignore-ssl-errors=true'\
            )
            browser = PhantomJS(self.config["phantomjs_path"], service_args=service_args)

            return browser


class WebDriverManager(object):

    # Config setting to use new webdriver instance per thread.
    ENABLE_THREADING_SUPPORT = "browser["threaded"]"

    # Config setting to reuse browser instances between WebdriverManager.new_driver() calls.
    INSTANCES = "browser["instances"]"


    def __init__(self, config, webdriver_factory):
        with open('config.json') as config:
            data = json.load(config)
        self.config = data
        self.__webdriver = {}  # Object with channel as a key
        self.__registered_drivers = {}
        self._webdriver_factory = WebDriverFactory()

    def get_driver(self):
        """
        Get an already running instance of Webdriver. If there is none, it will create one.

        Returns:
            Webdriver - Selenium Webdriver instance.
        """
        driver = self.__get_driver_for_channel(self.__get_channel())
        if driver is None:
            driver = self.new_driver()

        return driver

    def is_driver_available(self):
        """
        Check if a webdriver instance is created.

        Returns:
            bool - True, webdriver is available; False, webdriver not yet initialized.
        """
        channel = self.__get_channel()
        try:
            return self.__webdriver[channel] != None
        except:
            return False

    def new_driver(self):
        """
        Used at a start of a test to get a new instance of WebDriver.  If the
        'reusebrowser' setting is true, it will use a recycled WebDriver instance
        with delete_all_cookies() called.

        Returns:
            Webdriver - Selenium Webdriver instance.
        """
        channel = self.__get_channel()

        # Get reference for the current driver.
        driver = self.__get_driver_for_channel(channel)

      # if self.__config.get(WebDriverManager.REUSE_BROWSER, True):
            if driver is None:
                driver = self._webdriver_factory.create_webdriver(# global browser setting)

                # Register webdriver so it can be retrieved by the manager and
                # cleaned up after exit.
                self.__register_driver(channel, driver)
            else:
                try:
                    driver.quit()
                except:
                    pass

                driver = self._webdriver_factory.create_webdriver(# global browser name)
                self.__register_driver(channel, driver)

        else:
            # Attempt to tear down any existing webdriver.
            if driver is not None:
                try:
                    driver.quit()
                except:
                    pass
            self.__unregister_driver(channel)
            driver = self._webdriver_factory.create_webdriver(# global browser)
            self.__register_driver(channel, driver)

        return driver
        # End of new_driver method.

    def __register_driver(self, channel, webdriver):
        """ Register webdriver to a channel. """
        # Add to list of webdrivers to cleanup.
        if not self.__registered_drivers.has_key(channel):
            self.__registered_drivers[channel] = []  # set to new empty array

        self.__registered_drivers[channel].append(webdriver)

        # Set singleton instance for the channel
        self.__webdriver[channel] = webdriver

    def __unregister_driver(self, channel):
        """ Unregister webdriver """
        driver = self.__get_driver_for_channel(channel)

        if self.__registered_drivers.has_key(channel) \
                and driver in self.__registered_drivers[channel]:

            self.__registered_drivers[channel].remove(driver)

        self.__webdriver[channel] = None

    def __get_driver_for_channel(self, channel):
        """Get webdriver for channel"""
        try:
            return self.__webdriver[channel]
        except:
            return None

    def __get_channel(self):
        """Get the channel to register webdriver to."""

        if self.__config.get(WebDriverManager.ENABLE_THREADING_SUPPORT, False):
            channel = current_thread().ident
        else:
            channel = 0

        return channel

    def __del__(self):
        "Deconstructor, call cleanup drivers."
        try:
            self.clean_up_webdrivers()
        except:
            pass


class WebDriverAPI(object):
    """
    Provides a necessary higher-abstraction wrapper around selenium WebDriver
    """

    def __init__(self, browser):
        self.browser = WebDriverManager.get_driver()

    @staticmethod
    def get_base_url(webdriver):
        """
        Get the current base URL.

        Args:
            webdriver: Selenium WebDriver instance.

        Returns:
            str - base URL.
        """
        current_url = webdriver.current_url
        try:
            return re.findall("^[^/]+//[^/$]+", current_url)[0]
        except:
            raise RuntimeError(
                u("Unable to process base url: {0}").format(current_url))

    @staticmethod
    def get_browser_datetime(webdriver):
        """
        Get the current date/time on the web browser as a Python datetime object.
        This date matches 'new Date();' when ran in JavaScript console.
        Args:
            webdriver: Selenium WebDriver instance

        Returns:
            datetime - Python datetime object.
        """
        js_stmt = """
            var wtf_get_date = new Date();
            return {'month':wtf_get_date.getMonth(),
                    'day':wtf_get_date.getDate(),
                    'year':wtf_get_date.getFullYear(),
                    'hours':wtf_get_date.getHours(),
                    'minutes':wtf_get_date.getMinutes(),
                    'seconds':wtf_get_date.getSeconds(),
                    'milliseconds':wtf_get_date.getMilliseconds()};
        """
        date = webdriver.execute_script(js_stmt)
        return datetime(int(date['year']),
                        int(date['month']) + 1,  # javascript months start at 0
                        int(date['day']),
                        int(date['hours']),
                        int(date['minutes']),
                        int(date['seconds']),
                        int(date['milliseconds']))

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

    def dom(self):
        return self.browser.page_source

# Later define it in the user profiles, or take from owtf general.cfg
DEFAULT_ELEMENTS = ["a", "button", "li", "nav", "ol", "span", "ul", "header", "footer", "section"]

    def extractPath(self):
        """
        + Method to get clickable elements from browser DOM (using XPath)
        + List of eligible elements will come from config file
        """

        tree = html.fromstring(self.dom)

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


class WebElementSelector(object):
    """Utiltiy class for selecting elements."""

    @staticmethod
    def find_element_by_selectors(webdriver, *selectors):
        """
        Utility method makes it easier to find an element using multiple selectors. This is
        useful for problematic elements what might works with one browser, but fail in another.
        (Like different page elements being served up for different browsers)

        Args:
            selectors - var arg if N number of selectors to match against.  Each selector should
                        be a Selenium 'By' object.

        Usage::
            my_element = WebElementSelector.find_element_by_selectors(webdriver,
                                                                    (By.ID, "MyElementID"),
                                                                    (By.CSS, "MyClassSelector") )

        """
        # perform initial check to verify selectors are valid by statements.
        for selector in selectors:
            (by_method, value) = selector
            if not WebElementSelector.__is_valid_by_type(by_method):
                raise BadSelectorError(
                    "Selectors should be of type selenium.webdriver.common.by.By")
            if type(value) != str:
                raise BadSelectorError(
                    "Selectors should be of type selenium.webdriver.common.by.By")

        selectors_used = []
        for selector in selectors:
            (by_method, value) = selector
            selectors_used.append(
                "{by}:{value}").format(by=by_method, value=value)
            try:
                return webdriver.find_element(by=by_method, value=value)
            except:
                pass

        raise ElementNotSelectableException(
            "Unable to find elements using:") + u(",").join(selectors_used)

    @staticmethod
    def __is_valid_by_type(by_type):
        for attr, value in By.__dict__.iteritems():
            if "__" not in attr:
                if by_type == value:
                    return True

        return False
