#!/usr/bin/env python2
# -*- coding: utf-8 -*-


from utils import dom_utils
from main import Core

from lxml import html
from selenium.webdriver import *
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import *
from selenium.webdriver.support.ui import WebDriverWait


class Spider(object):
    """
    This is the main crawling engine.
      + It will use the robot (browser) module to do the crawling
        and will pass on the DOM tree for analysis.
      + The state module will provide the necessary functions for
        creating state-flow graph.
    """

    def __init__(self, Core, depth, base_url):
        self.Core = Core
        self.base = base_url
        self.depth = crawlDepth
        self.browser = 

    def main(self):
        """ Main crawler which loads the page, and simulated user actions. """
        self.browser.gotoURL(base_url)

