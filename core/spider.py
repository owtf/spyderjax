#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from lxml import html

from utils import dom_utils
from main import Core


class Spider(object):
    """
    This is the main crawling engine.
      - It will use the robot (browser) module to do the crawling
        and will pass on the DOM tree for analysis.
      - The state module will provide the necessary functions for
        creating state-flow graph.
    """

    def __init__(self, Core, depth, base_url):
        self.core = Core
        self.base = Core.Config["target"]
        self.depth = Core.Config["crawl_depth"]
