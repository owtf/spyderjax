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
from datetime import datetime
import random
import string

from six import u

from operator import itemgetter
from __future__ import generators


def generate_timestamped_string(subject="test", number_of_random_chars=4):
    """
    Generate time-stamped string. Format as follows...

    `2013-01-31_14:12:23_SubjectString_a3Zg`


    Kwargs:
        subject (str): String to use as subject.
        number_of_random_chars (int) : Number of random characters to append.

    + This method is helpful for creating unique names with timestamps in them
    """
    random_str = generate_random_string(number_of_random_chars)
    timestamp = generate_timestamp()
    return u"{timestamp}_{subject}_{random_str}".format(timestamp=timestamp,
                                                        subject=subject,
                                                        random_str=random_str)

def generate_timestamp(date_format="%Y-%m-%d_%H.%M.%S"):
    """
    Returns timestamped string. '2012-03-15_14:42:23

    Kwargs:
        format: A date/time format string.  If not specified, the default will be used.

    """
    return datetime.now().strftime(date_format)


def generate_random_string(number_of_random_chars=8, character_set=string.ascii_letters):
    """
    Generate a series of random characters.

    Kwargs:
        number_of_random_chars (int) : Number of characters long
        character_set (str): Specify a character set.  Default is ASCII
    """
    return u('').join(random.choice(character_set)
                      for _ in range(number_of_random_chars))

# Sample algorithm implementation
# Full detail given here: https://github.com/Pent00/YenKSP


# Computes K-Shortest Paths using Yen's Algorithm.
#
# Yen's algorithm computes single-source K-shortest loopless paths for a graph 
# with non-negative edge cost. The algorithm was published by Jin Y. Yen in 1971
# and implores any shortest path algorithm to find the best path, then proceeds 
# to find K-1 deviations of the best path.

## Computes K paths from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param start The source node of the graph.
# @param sink The sink node of the graph.
# @param K The amount of paths being computed.
#
# @retval [] Array of paths, where [0] is the shortest, [1] is the next 
# shortest, and so on.
#
def ksp_yen(graph, node_start, node_end, max_k=2):
    distances, previous = dijkstra(graph, node_start)
    
    A = [{'cost': distances[node_end], 
          'path': path(previous, node_start, node_end)}]
    B = []
    
    if not A[0]['path']: return A
    
    for k in range(1, max_k):
        for i in range(0, len(A[-1]['path']) - 1):
            node_spur = A[-1]['path'][i]
            path_root = A[-1]['path'][:i+1]
            
            edges_removed = []
            for path_k in A:
                curr_path = path_k['path']
                if len(curr_path) > i and path_root == curr_path[:i+1]:
                    cost = graph.remove_edge(curr_path[i], curr_path[i+1])
                    if cost == -1:
                        continue
                    edges_removed.append([curr_path[i], curr_path[i+1], cost])
            
            path_spur = dijkstra(graph, node_spur, node_end)
            
            if path_spur['path']:
                path_total = path_root[:-1] + path_spur['path']
                dist_total = distances[node_spur] + path_spur['cost']
                potential_k = {'cost': dist_total, 'path': path_total}
            
                if not (potential_k in B):
                    B.append(potential_k)
            
            for edge in edges_removed:
                graph.add_edge(edge[0], edge[1], edge[2])
        
        if len(B):
            B = sorted(B, key=itemgetter('cost'))
            A.append(B[0])
            B.pop(0)
        else:
            break
    
    return A

## Computes the shortest path from a source to a sink in the supplied graph.
#
# @param graph A digraph of class Graph.
# @param node_start The source node of the graph.
# @param node_end The sink node of the graph.
#
# @retval {} Dictionary of path and cost or if the node_end is not specified,
# the distances and previous lists are returned.
#
def dijkstra(graph, node_start, node_end=None):
    distances = {}      
    previous = {}       
    Q = priorityDictionary()
    
    for v in graph:
        distances[v] = graph.INFINITY
        previous[v] = graph.UNDEFINDED
        Q[v] = graph.INFINITY
    
    distances[node_start] = 0
    Q[node_start] = 0
    
    for v in Q:
        if v == node_end: break

        for u in graph[v]:
            cost_vu = distances[v] + graph[v][u]
            
            if cost_vu < distances[u]:
                distances[u] = cost_vu
                Q[u] = cost_vu
                previous[u] = v

    if node_end:
        return {'cost': distances[node_end], 
                'path': path(previous, node_start, node_end)}
    else:
        return (distances, previous)


class priorityDictionary(dict):
    def __init__(self):
        '''Initialize priorityDictionary by creating binary heap of pairs 
        (value,key).  Note that changing or removing a dict entry will not 
        remove the old pair from the heap until it is found by smallest() or
        until the heap is rebuilt.'''
        self.__heap = []
        dict.__init__(self)

    def smallest(self):
        '''Find smallest item after removing deleted items from heap.'''
        if len(self) == 0:
            raise IndexError, "smallest of empty priorityDictionary"
        heap = self.__heap
        while heap[0][1] not in self or self[heap[0][1]] != heap[0][0]:
            lastItem = heap.pop()
            insertionPoint = 0
            while 1:
                smallChild = 2*insertionPoint+1
                if smallChild+1 < len(heap) and \
                        heap[smallChild] > heap[smallChild+1]:
                    smallChild += 1
                if smallChild >= len(heap) or lastItem <= heap[smallChild]:
                    heap[insertionPoint] = lastItem
                    break
                heap[insertionPoint] = heap[smallChild]
                insertionPoint = smallChild
        return heap[0][1]

    def __iter__(self):
        '''Create destructive sorted iterator of priorityDictionary.'''
        def iterfn():
            while len(self) > 0:
                x = self.smallest()
                yield x
                del self[x]
        return iterfn()

    def __setitem__(self,key,val):
        '''Change value stored in dictionary and add corresponding pair to heap.  
        Rebuilds the heap if the number of deleted items grows too large, to 
        avoid memory leakage.'''
        dict.__setitem__(self,key,val)
        heap = self.__heap
        if len(heap) > 2 * len(self):
            self.__heap = [(v,k) for k,v in self.iteritems()]
            self.__heap.sort()  # builtin sort likely faster than O(n) heapify
        else:
            newPair = (val,key)
            insertionPoint = len(heap)
            heap.append(None)
            while insertionPoint > 0 and \
                    newPair < heap[(insertionPoint-1)//2]:
                heap[insertionPoint] = heap[(insertionPoint-1)//2]
                insertionPoint = (insertionPoint-1)//2
            heap[insertionPoint] = newPair

    def setdefault(self,key,val):
        '''Reimplement setdefault to call our customized __setitem__.'''
        if key not in self:
            self[key] = val
        return self[key]
