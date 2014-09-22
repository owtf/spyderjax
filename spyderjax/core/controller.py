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

* This module defines a controller which manages the start, pause and stop
  process of the robot.
'''

import simplejson as json
import subprocess
from glob import glob
from Queue import Queue
import threading

from main import Core
from embedded_browser import Browser


threads = []  # contains handles for each thread
q = Queue()  # The main queue.
output = Queue()  # The output queue - prevents output overlap


class OutThread(threading.Thread):  # Worker thread that takes care of output
    def __init__(self, Core, queue, logfile):
        threading.Thread.__init__(self)
        self.queue = queue
        self.logfile = os.path.join(self.core.RootDir, 'output/output.log')
        self.core = Core

    def run(self):
        while True:
            writelog(self.queue.get(), self.logfile)
            self.queue.task_done()


class Control(object):
        """ Mainly manages the browser instances."""
    def __init__(self, Core, desired_capabilities=None):
        self.core = Core
        self.pool = {}

    def get_all(self):
        return self.pool

"""
def run():
    """Make the crawler run in mutiple browser instances. """

    def wrapper(*args, **kwargs):
        threads = []
        queue = multiprocessing.Queue(len(args[0].drivers._desired_capabilities) + 1)
        i = 0

        if not hasattr(args[0].drivers, "_drivers"):
            for c in args[0].drivers._desired_capabilities:
                kwargs = {'desired_capabilities': c}

                if args[0].drivers._command_executor != None:
                    kwargs['command_executor'] = args[0].drivers._command_executor

                driver = webdriver.Remote(**kwargs)
                args[0].drivers.register(driver)

        for d in args[0].drivers._drivers:
            t = multiprocessing.Process(target=thread_func, args=(test, d))
            t.start()
            threads += [t]

        for t in threads:
            t.join()


    return wrapper
"""
