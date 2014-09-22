#!/usr/bin/env python
# -*- coding: utf-8 -*-

from lxml import html
from splinter import Browser
from subprocess import Popen

from utils import dom_utils
from main import Core
from embedded_browser import Browser
from state_machine import StateMachine


class Spider(object):
    """
    This is the main crawling engine.
      - It will use the robot (browser) module to do the crawling
        and will pass on the DOM tree for analysis.
      - The state module will provide the necessary functions for
        creating state-flow graph.
    """

    def __init__(self, Core):
        self.core = Core
        self.base_url = Core.Config["target"]
        self.allowed_domains = ['.'.join(self.base_url.split('.')[-2:])] # adding [] around the value seems to allow it to crawl subdomain of value
        self.browser = Browser.create()
        self.state_machine = StateMachine()
        #self.browser_instances = Core.Config["browser"]["instances"]
        #self.pool = []

    def crawl(self):
        # get the base url and save the DOM as a txt file in the scans output
        self.browser.visit(self.base_url)
        self.browser.
