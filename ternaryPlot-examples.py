# -*- coding: utf-8 -*-
"""
Created on Mon Mar  8 16:43:42 2021

@author: ustcw
"""
from pyTernary.ternaryPlot import TernaryPlot
import numpy as np
import matplotlib.pyplot as plt

#%%

plt.rcParams["lines.markersize"] = 8
tp = TernaryPlot(scale = 1)
fig, ax = plt.subplots()
fig.set_size_inches(8, 8*np.sqrt(3)/2)
interval = 0.1
tick_len = 0.015

np.random.seed(33)

data1 = np.concatenate((np.random.rand(100, 1), np.random.rand(100, 1)/8, np.random.rand(100, 1)/16), axis = 1)
data1 = data1/np.sum(data1, axis = 1)[:, None]

np.random.seed(55)
data2 = np.concatenate((np.random.rand(100, 1)/8, np.random.rand(100, 1), np.random.rand(100, 1)/16), axis = 1)
data2 = data2/np.sum(data2, axis = 1)[:, None]

tp.set_boundary(ax = ax)
tp.set_gridlines(ax = ax, interval = interval)
tp.set_axis_status(ax, status = "off")
#tp.set_axis_ticks_BRL(ax, tick_rotation = 0, tick_interval = interval, tick_length = tick_len)
#tp.set_ticks_label_BRL(ax, label_rotation = 0, tick_interval = interval, offdis = 2.5*tick_len)
#
#tp.set_left_corner_label(ax, label = "1", offdis = 5*tick_len, rotation = 0)
#tp.set_right_corner_label(ax, label = "2", offdis = 5*tick_len, rotation = 0)
#tp.set_top_corner_label(ax, label = "3", offdis = 5*tick_len, rotation = 0)

# set ticks adn tick labels for bottom and left axis
tp.set_axis_ticks_BL(ax, tick_rotation = 0, tick_interval = interval, tick_length = tick_len)
tp.set_ticks_label_BL(ax, label_rotation = 0, tick_interval = interval, offdis = 2.5*tick_len)

# set axis labels
tp.set_bottom_axis_label(ax, label = "mole percent of A", offdis = 0.05, rotation = 0)
tp.set_left_axis_label(ax, label = "mole percent of B", offdis = 0.05, rotation = 0)

a1, = tp.plot(data1, ax, color = "b", marker = 'o', linewidth = 0, label = "data1")
b1, = tp.plot(data2, ax, color = "r", marker = 's', linewidth = 0, label = "data2")

#a1.set_label("A")
#b1.set_label("B")
#ax.legend()
#tp.legend(ax)
tp.show_legend(ax, fontsize = 16, bbox_to_anchor = (0.5, 0.5, 0.5, 0.5))

#fig.savefig("Phase Diagram data.png", dpi = 400)
#%%

tp = TernaryPlot(scale = 1)
fig, ax = plt.subplots()
fig.set_size_inches(8, 8*np.sqrt(3)/2)

tp.set_boundary(ax = ax)
tp.set_gridlines(ax = ax, interval = interval)
tp.set_axis_status(ax, status = "off")

startpoint = "left"
axisrange = [[1, 0, 0], [0.6, 0.4, 0], [0.7, 0, 0.3]]

data_select1 = data1[data1[:, 0] > 0.6]
data_select2 = data2[data2[:, 0] > 0.6]

a2, = tp.zoomin_plot(data_select1, axis_range = axisrange, ax =ax, color = "b", marker = 'o', linewidth = 0, label = "data1")
b2, = tp.zoomin_plot(data_select2, axis_range = axisrange, ax =ax, color = "r", marker = 's', linewidth = 0, label = "data2")
#(a2, b2), ("data 1", "data 2"), 
tp.show_legend(ax, fontsize= 16, bbox_to_anchor = (0.5, 0.5, 0.5, 0.5))

tp.set_zoomin_axis_ticks_bilateral(ax, startpoint = startpoint)
tp.set_zoomin_ticks_label_bilateral(axis_range = axisrange, ax=ax,  startpoint = startpoint, offdis = 0.05)

tp.set_bottom_axis_label(ax, label = "mole percent of A", offdis = 0.05, rotation = 0)
tp.set_left_axis_label(ax, label = "mole percent of B", offdis = 0.05, rotation = 0)

#axisrange = [[0.5, 0, 0.5], [0, 0.5, 0.5], [0, 0, 1]]
#axisrange =  np.array([[1, 0, 0], [0, 0.5, 0.5], [0, 0, 1]])
#axisrange = [[0.4, 0, 0.6], [0, 0.6, 0.4], [0, 0, 1]]
#
#st = "top"
#axisrange = [[0.6, 0, 0.4], [0, 0.4, 0.6], [0, 0, 1]] # top
#data0 = axisrange + [[0.3, 0.1, 0.6]]
#st = "right"
#axisrange = [[0.8, 0.2, 0], [0, 1, 0], [0, 0.5, 0.5]] # right
#data0 = axisrange + [[0.3, 0.6, 0.1], [0.35, 0.55, 0.1]]
#
#st = "right"
#axisrange = [[0.6, 0.4, 0], [0, 1, 0], [0, 0.5, 0.5]] # right
#data0 = axisrange + [[0.3, 0.6, 0.1]]
#data0  = np.array(data0)
#st = "left"
#axisrange = [[1, 0, 0], [0.3, 0.7, 0], [0.8, 0, 0.2]] # left
#data0 = axisrange + [[0.8, 0.1, 0.1]]
#
#tp.ternary_plot(data0, ax, interval = 0.1, label_rotation = [30, 30, -30])
#tp.ternary_zoomin_plot(data0, axis_range = axisrange, startpoint = st, interval = 0.1, label_rotation = [0, 0, 0])
#    tp.ternary_zoomin_plot([0.3, 0.1, 0.6], ax = ax, axis_range = axisrange, interval = 0.1, label_rotation = [0, 0, 0])
#    tp.set_axis_status(ax, status = "on")
#axis_conv = coordinates_conversion(axisrange)