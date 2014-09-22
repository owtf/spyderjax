#!/usr/bin/env python2
# -*- coding: utf-8 -*-
import splinter
from lxml import html


def crawl_action(event, element):
    return {"event"=event, "candidate_element"=element}
