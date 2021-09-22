# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 10:57:20 2021

@author: ustcw
"""

import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt

# plt.rcParams["lines.markersize"] = 4
# plt.rcParams["markers.fillstyle"] = "none"
plt.rcParams["font.size"] = 16
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14

def colormap2d(array, figsize = 12, datatype_name = "", **kwargs):
    """
    To map a 2d array.
    
    array: 2-d array;
    figsize: int, the size of figure;
    datatype_name: the meaning of data and also the name for title;
    
    Returns
    -------
    None.

    """
    
    if (not isinstance(array, np.ndarray)):
        if (isinstance(array, list)):
            array = np.array(array)
        else: raise TypeError("array is neither an array-type or list-type.")
    if "cmap" not in kwargs.keys():
        kwargs["cmap"] = "gist_rainbow"
    sorted_count = np.sort(array.ravel())
    vmin = np.floor(np.average(sorted_count[:100]))
    vmax = np.ceil(np.average(sorted_count[-100:]))
    width = array.shape[1]
    height = array.shape[0]
    
    fig = plt.figure(figsize = (figsize*width/(width + height), figsize*height/(width + height))) #figsize = (10, 6)
    left = 0.08
    right = 0.9
    top = 0.9
    bottom = 0.08
    fig.subplots_adjust(left = left, right = right, top = top, bottom = bottom)
    ax = fig.add_subplot(111)
    p = ax.imshow(array, vmin = vmin, vmax= vmax, **kwargs) #"gist_rainbow"
    # ax.colorbar()
    colorbar_left = right + 0.01
    colorbar_bottom = bottom
    colorbar_width = 0.02
    colorbar_height = top - bottom
    
    cb_ax = fig.add_axes([colorbar_left, colorbar_bottom, colorbar_width, colorbar_height])
    fig.colorbar(p, cax = cb_ax)
    # plt.title("Distribution of counts {}".format(comps[elem_id]))
    if (datatype_name != "") :
        ax.set_title("EDS mapping of {}".format(datatype_name))

def moving_average_1d(x, w, mode = "valid"):
    """
    x: 1d array;
    w: int type, window size;
    mode: convolve mode for np.convolve function;
    
    return: convolved array;
    """
    return np.convolve(x, np.ones(w), mode) / w

def moving_average_2d(a, w, mode = str):
    return convolve2d(a, np.ones((w,w)), mode = mode)/w/w

def get_data_at_pixel(data, pos):
    """
    data: nx3 size, list or array;
    pos: positions where to get data;
    
    return array.
    """
    arr = []
    for i in pos:
        arr.append([data[0][i], data[1][i], data[2][i]])
        
    return np.array(arr)

def points_stats(data):
    data_set = {}
    for i in range(101):
        for j in range(101 - i):
            data_set[(i, j, 100-i-j)] = 0
            
    for i in range(len(data)):
        if (np.isnan(data[i, 0])): continue
        a = round(data[i, 0])
        b = round(data[i, 1])
        c = 100 - a - b
        data_set[(a, b, c)] += 1
        
    return data_set

