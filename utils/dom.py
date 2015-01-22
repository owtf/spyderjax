#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import re
import sys
from lxml import html

from core.lib.readability import cleaners


def normalize(html):
    """Normalize the input HTML using the execellent readability library. """
    return str(cleaners.html_cleaner.clean_html(html))

# DOM equivalence algorithm
def isequivalent(dom1, dom2):
    hash1 = hashcode(normalize(dom1))
    hash2 = hashcode(normalize(dom2))

    if hash1 == hash2:
        return True
    else:
        return False

def parse(html):
    """
    # This will convert the html source into a dom object
    # Note that browser interaction is always done on the original DOM, not the modified dom."""
    # Convert html source to dom object
    # Error catching because of badly formatted HTML, although lxml tends to perform very well :)
    try:
        tree = html.fromstring(normalize(html))
        return tree
    except:
        print("Error in parsing HTML..")

def xpath(expression):
    return self.tree.xpath(expression)
  
def css_select(self, expression, text = False):
    sel = CSSSelector(expression)
    selected_elements = sel(self.tree)
    if text:
       selected_elements = map(lambda x: x.text, selected_elements)
    return selected_elements

# Computes a hashcode from string to compare if 2 DOMs are equivalent
def hashcode(string):
    """ Calculates a hash based on html string. """
    return hashlib.md5(string).hexdigest()

# Implemented in crawljax; not too efficient
# too uptight on equivalence - would probably lead to state explosion
def levenshtein(string1, string2):
    """
    # Measures the amount of difference between two strings.
    # The return value is the number of operations (insert, delete, replace)
      required to transform string a into string b.
    """
    # http://hetland.org/coding/python/levenshtein.py
    n, m = len(string1), len(string2)
    if n > m:
        # Make sure n <= m to use O(min(n,m)) space.
        string1, string2, n, m = string2, string1, m, n
    current = range(n+1)
    for i in xrange(1, m+1):
        previous, current = current, [i]+[0]*n
        for j in xrange(1, n+1):
            insert, delete, replace = previous[j]+1, current[j-1]+1, previous[j-1]
            if string1[j-1] != string2[i-1]:
                replace += 1
            current[j] = min(insert, delete, replace)
    return current[n]

def minEditDist(dom1, dom2):
    """
    # Implements the edit-distance method on DOM for backtracking and DOM diff measure
    # Computes the min edit distance from target to source
    # Stolen from http://www.cs.colorado.edu/~martin/csci5832/edit-dist-blurb.html. """
    n = len(dom1)
    m = len(dom2)

    distance = [[0 for i in range(m+1)] for j in range(n+1)]

    for i in range(1,n+1):
        distance[i][0] = distance[i-1][0] + insertCost(dom2[i-1])

    for j in range(1,m+1):
        distance[0][j] = distance[0][j-1] + deleteCost(dom1[j-1])

    for i in range(1,n+1):
        for j in range(1,m+1):
           distance[i][j] = min(distance[i-1][j]+1,
                                distance[i][j-1]+1,
                                distance[i-1][j-1]+substCost(dom1[j-1],dom2[i-1]))
    return distance[n][m]

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
