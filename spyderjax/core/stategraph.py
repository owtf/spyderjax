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
  process of the robot and the state-flow graph engine
'''
import multiprocessing import process, lock
from lxml import html
import networkx as nx

from main import Core
from utils import dom_utils

eventable = [original_state, final_state, event]


class state(object):
    """
    * The state vertex class which represents a state in the browser. When iterating over the possible
    * candidate elements every time a candidate is returned its removed from the list so it is a one
    * time only access to the candidates.
    """

    def __init__(self, id, dom, url, name=None, candidate_elements=None):
        self.id = id
        self.dom = dom
        self.stripped_dom = dom_utils.normalize(dom)
        self.url = url
        self.name = name
        self.candidate_elements = candidate_elements
        self.visited = False


class StateFlowGraph(object):
    """
    Defines a event flow graph for DOM states
      - The State-Flow Graph is a multi-edge directed graph with states (StateVetex) on the vertices and
      - clickables (Eventable) on the edges.
    """

    def __init__(self, Core):
        self.Core = Core
        self.sfg = nx.MultiDigraph()   # the graph is a multi-edged directed graph
        self.states = {}
        self.edges = {}

    def add_event(self, initial_node, final_node, event):
        """
        * Adds the specified edge to this graph, going from the source vertex to the target vertex.
        * More formally, adds the specified edge, e, to this graph if this graph contains no edge e2
        * such that e2.equals(e). If this graph already contains such an edge, the call leaves this
        * graph unchanged and returns false. Some graphs do not allow edge-multiplicity. In such cases,
        * if the graph already contains an edge from the specified source to the specified target, than
        * this method does not change the graph and returns false. If the edge was added to the graph,
        * returns true. The source and target vertices must already be contained in this graph.
        """
        self.Core.logger.info('Adding the edge')
        if self.sfg.has_edge(initial_node, final_node):
            return False
        else:
            self.sfg.add_edge(initial_node, final_node, event)

    def add_state(self, state):
        self.Core.logger.info('Adding a new state')
        if sfg.has_node(state.id):
            return False # to speed up, this can also be written as if state.id in self.sfg
        else:
            self.sfg.add_node()

    def get_clickables(self, state):
        return self.sfg.get_node_attributes(state.id)

    def can_goto(self, source, target):
        """ Boolean for existence of an edge. """
        # both conditions check because sfg is a directed graph
        if self.sfg.has_edge(source, target) or self.sfg.has_edge(target, source):
            return True
        else:
            return False

    def get_shortest_path(self, start, end):
        # get the shortestpath using the DijkstraShortestPath algorithm

        return nx.shortest_path(self.sfg, start, end)

    def get_all_states(self):
        # in fact, get all nodes as a list
        return self.sfg.nodes()

    def get_all_possible_paths(self, start):
        return nx.single_source_shortest_path_length(self.sfg, start)

    def visited_states(self, state):
        # check the visited flag in the state attributes
        visited = []
        for state in self.sfg:
            if state.visited:
                state.append(visited)
            else:
                pass
