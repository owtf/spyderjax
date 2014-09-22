#!/usr/bin/python2
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
import copy
import functools
import mimetypes
from lxml import html

from main import Core

import splinter

from selenium.webdriver.support import wait
from utils.webdriver_patches import patch_webdriver
from utils.splinter_patches import patch_webdriverelement


class Browser(object):
    """Emulate splinter's Browser."""

    def __init__(self, Core, *args, **kwargs):
        #self.driver = create()
        self.core = Core

    def create(self):
        # handle like a switch case
        if self.core.Config["driver"] == "firefox":
            profile = FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", "127.0.0.1")
            profile.set_preference("network.proxy.http_port", "8008")
            profile.set_preference("network.proxy.no_proxies_on", "")
            profile.set_preference('webdriver_enable_native_events', True)
            profile.update_preferences()
            browser = splinter.Browser('firefox', firefox_profile=profile)

            return browser

        elif self.core.Config["driver"] == "chrome":
            options = ChromeOptions()
            options.add_arguments("--proxy-server=http://127.0.0.1:8008/")
            browser = splinter.Browser('chrome',
                                        executable_path=self.core.Config["chromedriver_path"]
                                      )

            return browser

        elif self.core.Config["driver"] == "phantomjs":
            service_args = (
                            '--proxy=127.0.0.1:8008',
                            '--proxy-type=https',
                            '--ignore-ssl-errors=true'
                           )

            browser = splinter.Browser('phantomjs',
                                        self.core.Config["phantomjs_path"],
                                        service_args=service_args
                                      )

            return browser

    def wait_for_condition(self, condition=None, timeout=None, poll_frequency=0.5, ignored_exceptions=None):
        """Wait for given javascript condition."""
        condition = functools.partial(condition or self.visit_condition, self)

        timeout = timeout or self.visit_condition_timeout

        return wait.WebDriverWait(self.driver,
                                  timeout,
                                  poll_frequency=poll_frequency,
                                  ignored_exceptions=ignored_exceptions
                                 ).until(lambda browser: condition())

    # Later define it in the user profiles, or take from owtf general.cfg
    DEFAULT_ELEMENTS = ["a", "button", "li", "nav", "ol", "span", "ul", "header", "footer", "section"]

    def get_path(self):
        """
        Method to get clickable elements from browser DOM (using XPath)
        List of eligible elements will come from config file
        """
        clicable_element_types = tuple('%s[not(contains(@class, "selenium_donotclick"))]' % i for i in (
            'a', 'submit', 'input[@type="submit"]',
        ))
        xpath = '|'.join('//%s' % item for item in clicable_element_types)
