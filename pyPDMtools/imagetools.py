# -*- coding: utf-8 -*-
"""
Created on Mon Dec 20 11:12:58 2021

@author: ustcw
"""

import sys

#from pyTernary.ternaryPlot import TernaryPlot
#from pyTernary.plots import ternary_plot, tielines_plot
import EDS_mapping as eds
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseButton

#%%
# plt.rcParams["lines.markersize"] = 4
# plt.rcParams["markers.fillstyle"] = "none"
plt.rcParams["font.size"] = 16
plt.rcParams["xtick.labelsize"] = 14
plt.rcParams["ytick.labelsize"] = 14

class LineBuilder:
    def __init__(self, line, fig):
        self.line = line
        self.fig = fig
        self.coords = []
        self.cid = line.figure.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        try:
            zooming_panning = ( self.fig.canvas.cursor().shape() != 0 ) # 0 is the arrow, which means we are not zooming or panning.
        except:
            zooming_panning = False
        if zooming_panning:
            print("Zooming or panning")
            return
        if event.button==3:
            print('clean up')
            event.canvas.mpl_disconnect(self.cid)
            return
        else:
             ix, iy = event.xdata, event.ydata
             print('x = %.3f, y = %.3f'%(ix, iy))
             self.coords.append(iy)
             
class ImageBuilder:
    """ To plot interactive composition versus distance profiles. """
    def __init__(self, fig, ax, data):
        """
        data: a DataFrame that has comps info.
        fig:
        ax:
        """
        self.fig = fig
        self.ax = ax
        self.data = data
        self.coords = []
        self.tempPoints = []
        self.tempLine = None
        self.linebuilder = [] #2-dimensional list.
        self.xy_coords = []
        self.cid = fig.canvas.mpl_connect('button_press_event', self)

    def __call__(self, event):
        try:
            zooming_panning = ( self.fig.canvas.cursor().shape() != 0 ) # 0 is the arrow, which means we are not zooming or panning.
        except:
            zooming_panning = False
        if zooming_panning:
            print("Zooming or panning")
            return
        """
        Button-1: left mouse button,
        Button-2: middle button,
        Button-3: rightmost button.
        """
        if event.button==3:
            if (len(self.coords) > 0) :
                [self.tempPoints[i].remove() for i in range(len(self.coords))]
                self.tempPoints.clear()
                self.coords.clear()
                if self.tempLine is not None:
                    self.tempLine.remove()
                    self.tempLine = None
#            time.sleep(0.1)
            plt.pause(0.1)
            print('Terminated.')
            event.canvas.mpl_disconnect(self.cid)
            return
        else:
            if len(self.linebuilder) >= 1:
                last_item = self.linebuilder[-1]
                flag = sum([len(ibs.coords) == 0 for ibs in last_item]) == len(last_item)
                if (flag): 
                    self.linebuilder.pop()
                    self.xy_coords.pop()
            if (len(self.coords) == 2) :
                self.coords.clear()
                self.tempPoints[0].remove()
                self.tempPoints[1].remove()
                self.tempPoints.clear()
                self.tempLine.remove()
                self.tempLine = None
            ix, iy = event.xdata, event.ydata
            line = self.ax.plot(ix, iy, marker = "s", color = "white", markersize = 6, markeredgecolor = "black", markeredgewidth = 2)
            plt.pause(0.1)
#             line = ax.scatter(100, 100, marker = "s", color = "white", s = 10)
            self.tempPoints.append(line[0])
            ix, iy = round(ix), round(iy)
            print('x = %d, y = %d'%(ix, iy))
            self.coords.append([ix, iy])
            if (len(self.coords) == 2):
                ix1, iy1 = self.coords[0]
                ix2, iy2 = self.coords[1]
                x, y = [], []
                if (ix2 - ix1 == 0):
                    direction = 1 if iy1 < iy2 else -1
                    y = list(range(iy1, iy2 + direction, direction))
                    x = [ix1] * len(y)
                elif (iy2 - iy1 == 0):
                    direction = 1 if ix1 < ix2 else -1
                    x = list(range(ix1, ix2 + direction, direction))
                    y = [iy1] * len(x)
                else :
                    slope = (iy2 - iy1)/(ix2 - ix1)
                    if (abs(slope) > 1) :    
                        direction = 1 if iy1 < iy2 else -1
                        y = list(range(iy1, iy2 + direction, direction))
                        x = [ix1 + direction * round(i / slope) for i in range(len(y))]
                    else:
                        direction = 1 if ix1 < ix2 else -1
                        x = list(range(ix1, ix2 + direction, direction))
                        y = [iy1 + direction * round(i * slope) for i in range(len(x))]
                locations = [x, y]
                points_list = np.array([np.linspace(ix1, ix2, 10), np.linspace(iy1, iy2, 10)]).T
                self.tempLine = self.ax.plot(*zip(*points_list), "k--")[0]
                plt.pause(0.1)
                lb = comps_data_plot(self.data, locations)
                self.xy_coords.append([(ix1, ix2), (iy1, iy2)]) 
                self.linebuilder.append(lb)
                


def comps_data_plot(data, locs = np.array([]), **kwargs) :
    """
    data: a dict includes comps info of arrays.
    locs: 2 X n dimensions. The pos of array where to plot the data.
    """
    comps = list(data.keys())
    plt_kwargs = {"marker": "o", "markersize": 10, "linewidth": 0, "label": None}
    plt_kwargs.update(kwargs)
    linebuilder = []
    for comp in comps:
        selected_data = data[comp][tuple(locs[1]), tuple(locs[0])] # using tuple to select data;
        fig, ax = plt.subplots()
        line, = ax.plot(range(len(selected_data)), selected_data, **plt_kwargs)
        linebuilder.append(LineBuilder(line, fig))
    #    plt.plot(index[data_line[comps[elem_id] + '_Anomaly']], data_line[comps[elem_id]][data_line[comps[elem_id] + '_Anomaly']], "ro")
        ax.set_xlabel("position of pixels")
        ax.set_ylabel(f"Compositions of {comp} (at./%)")
        plt.tight_layout()
        
    return linebuilder

def scan_line_plot(ax, data, **kwargs):
        plt_kwargs = {"linestyle": "--", "linewidth": 1, "color": "black", "label": None}
        plt_kwargs.update(kwargs)
        if len(data[0]) != 2: raise ValueError("the dimension of element in data is not equal to 2.")
        
        for dt in data:
            ax.plot(dt[0], dt[1], **plt_kwargs)
            

def remain_element_id(ids, elem_ids):
    for i in ids:
        if i not in elem_ids:
            return i
    
    return None

def find_empty_index(data):
    """
    data: A list of linebuilder objects;
    """
    for i, row in enumerate(data):
        if (len(row.coords) == 0): return i
    
    raise ValueError("No empty index found!")
    