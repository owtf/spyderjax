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
'''

from lxml import html

import main
from embedded_browser import 
import controller
from stategraph import StateFlowGraph
from utils import dom_utils


class StateMachine(object):
    """ The state machine class. """

    def __init__(self, Core, embedded_browser):
        self.Core = Core
        self.browser = embedded_browser

    def initialState(self):
        pass

    def currentState(self):
        return get_state_by_id(index[0])

    def newState(self):
        dom = self.browser.getDom()

        return stateFlowGraph.new_state(self.browser.get_base_url(),
                                        dom,
                                        dom_utils.normalize(dom)
                                )

    # ChangeS the currentState to the nextState if possible. The next state should already be
    # present in the graph.
    def changeState(self):
        if not nextState:
            return False

        if StateFlowGraph.can_goto(currentState, nextState):
            # next state becomes the current state
            currentState() = nextState();
            return True

        else:
            return False

    # Adds the newState and the edge between the currentState and the newState on the SFG.
    # SFG = stateFlowGraph
