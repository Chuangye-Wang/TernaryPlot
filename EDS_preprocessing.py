# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 12:00:56 2022

@author: ustcw
"""
from pyTernary.ternaryPlot import TernaryPlot
from pyTernary.plots import ternary_plot, tielines_plot
import pyTernary.EDS_mapping as eds
from pyTernary.EDS_data import EDS_data
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def enlarge_edges(edges, window_size = 1, edge_value = 255, delete_first_edge = False):
    if window_size == 0 and not delete_first_edge: return edges
    m, n = edges.shape
    new_edges = np.zeros((m, n))
    r = 2 * window_size + 1
    for i in range(window_size, m - window_size):
        for j in range(window_size, n - window_size):
            if edges[i, j] != edge_value: continue
            top = i - window_size
            left = j - window_size
            new_edges[top: top + r, left: left + r] = edge_value
            
    return new_edges


def find_non_edges_index(edges, edge_value = 255):
    m, n = edges.shape
    res = []
    for i in range(0, m):
        for j in range(0, n):
            if edges[i, j] == edge_value: continue
            res.append([i, j])
            
    return res


def find_non_cracks_index(edges, counts, threshold = 80):
    """ To remove the index of cracks in edges 
    edges: a list or array in (n, 2) shape
    counts: a dataframe, list or array, the quantitative signal/indensity at each scanning area.
    threshold: the index where values are smaller than the threshold will be dropped. This basically means that
    the probe scans at a crack, therefore the collected signal is weak.
    
    return: a list after removing low-count locations.
    """
    res = []
    if (isinstance(counts, (pd.DataFrame, list))): counts = np.array(counts)
    for item in edges:
        if (counts[item[0], item[1]] < threshold): continue
        res.append(item)
        
    return res
    

def select_non_crackAndEdge_data(eds_data, indexes, plot_order = [0, 1, 2]):
    """ Select data that are not at cracks and not at edges.
    
    data: pyTernary.EDS_data.EDS_data type.
    indexes: a list or array in (n, 2) shape. The indexes that are kept for selecting the data in a 
        2D matrix or the scanning area.
    plot_order: a list of 3 integers. It is the order of the three elements in the column of return list.
    
    return: an array.
    """
    res = []
    comps = eds_data.comps
    for item in non_crack_edge_index:
        res.append([eds_data.data[comps[plot_order[0]]][item[0]][item[1]],
                  eds_data.data[comps[plot_order[1]]][item[0]][item[1]],
                  eds_data.data[comps[plot_order[2]]][item[0]][item[1]]
                  ])
    
    return np.array(res)