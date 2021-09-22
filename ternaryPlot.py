# -*- coding: utf-8 -*-
"""
Created on Mon Feb 22 17:39:25 2021

@author: ustcw
"""

#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from decimal import Decimal

class TernaryPlot(object):
    def __init__(self, scale):
        """ Build a constructor with scale as the input parameter
        """
        self.scale = scale
    
    
    def set_scale(self, scale):
        """ To set the scale of plot.
        """
        self.scale = scale
    
    
    def get_scale(self):
        """ To get the scale of plot.
        """
        return self.scale
 
    
    def set_boundary(self, ax = None, **plt_kwargs):
        """ Plotting boundary lines for ternary diagram
        
        ax: ax canvas 
        plt_kwargs: a dict contains the options for plotting the boundary lines.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = "k"
        if "linewidth" not in plt_kwargs.keys():
            plt_kwargs["linewidth"] = 2
        
        boundary_points3 = np.array([[1,0,0], [0,1,0], [0,0,1], [1,0,0]]) * self.get_scale()
        boundary_points2 = self.coordinates_conversion(boundary_points3)
        ax.plot(boundary_points2[:, 0], boundary_points2[:, 1], label = None, **plt_kwargs)
    
    
    def zoomin_plot(self, data, axis_range = [], ax = None, **plt_kwargs):
        """ To transform axis range to [(1,0,0), (0,1,0), (0,0,1)] triangle.
        
        data: n x 3 dimensional list or array
        axis_range: a list or array with 3 x 3 dimension data points
        color: marker and line color
        marker: marker for datapoints
        linewidth: linewidth for plotted line
        plt_kwargs: a dict contains the options for plotting the datapoints
        
        Returns: ax plot.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
        if len(axis_range) == 0:
            raise ValueError("axisrange cannot be empty")
        for item in axis_range:
            if sum(item)/self.get_scale() != 1:
                raise ValueError("the sum of coordinates of one point not equal to 1")
        
        data_conv = self.coordinates_conversion(data)
        datapoints0 = np.array([(0, 0), (1, 0), (1/2, np.sqrt(3)/2)])*self.get_scale()
        x01, y01 = datapoints0[0]
        x02, y02 = datapoints0[1]
        x03, y03 = datapoints0[2]
        datapoints1 = self.coordinates_conversion(axis_range)
        x11, y11 = datapoints1[0]
        x12, y12 = datapoints1[1]
        x13, y13 = datapoints1[2]
        
        A = np.array([[x02 - x01, x03 - x01], [y02 - y01, y03 - y01]])
        B = np.array([[x12 - x11, x13 - x11], [y12 - y11, y13 - y11]])
        B = np.linalg.inv(B)
        data_zoomin = np.zeros((len(data_conv), 2))
        datapoints01 = np.array([x01, y01])
        datapoints11 = np.array([x11, y11])
    #    print(data_conv.shape, datapoints01.shape, data_zoomin.shape)
        for i in range(0, len(data_conv)):
            data_zoomin[i] = np.dot(np.dot(A, B), (data_conv[i] - datapoints11)) + datapoints01
        
    #    data_zoomin = data_zoomin.T
        return ax.plot(data_zoomin[:, 0], data_zoomin[:, 1], **plt_kwargs)
    
    
    def set_gridlines(self, ax = None, interval = 0.1, **plt_kwargs):
        """ Plotting gridlines in ternary diagram
        
        ax: matplotlib.axes._subplots.AxesSubplot
        interval: the gridlines interval shown in figure.
        plt_kwargs: a dict contains the options for plotting the gridlines.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        
        if "linewidth" not in plt_kwargs.keys():
            plt_kwargs["linewidth"] = 0.5
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = "k"
        if "linestyle" not in plt_kwargs.keys():
            plt_kwargs["linestyle"] = "--"
            
        lines_number = int(self.get_scale()/interval)
        lines_list = [i for i in range(1, lines_number)]
        line1 = np.array([[i*interval, self.get_scale() - i*interval, 0] for i in lines_list])
        line1_c = self.coordinates_conversion(line1)
        line2 = np.array([[0, i*interval, self.get_scale()-i*interval] for i in lines_list])
        line2_c = self.coordinates_conversion(line2)
        line3 = np.array([[i*interval, 0, self.get_scale()-i*interval] for i in lines_list])
        line3_c = self.coordinates_conversion(line3)
        
        line12_c = np.concatenate([line1_c, line2_c[::-1]], axis = 1)
        line23_c = np.concatenate([line2_c, line3_c], axis = 1)
        line31_c = np.concatenate([line3_c, line1_c], axis = 1)
        lines_all = np.concatenate([line12_c, line23_c, line31_c], axis = 0)
    
        for i in range(0, len(lines_all)):
            ax.plot(lines_all[i][0::2], lines_all[i][1::2], label = "", **plt_kwargs)
        
    
    def coordinates_conversion(self, x):
        """ Convert 3 dimensional coordinates to 2-dimension
        
        x: (n x 3) dimensional array or list, for each data point, it can also be ratio among each coordinate x,y,z
        
        Returns: an (n x 2) dimensional array
        """
        
        if isinstance(x, list):
            x = np.array(x)
#        print(x, type(x))
        if x.shape == (3,):
            x = x[None, :]
        x_conv = np.zeros((len(x), 2))
        for i in range(len(x)):
            x_conv[i, :] = [1/2*(2*x[i, 1] + x[i, 2])/(x[i, 0] + x[i, 1] + x[i, 2]), np.sqrt(3)/2*x[i, 2]/(x[i, 0] + x[i, 1] + x[i, 2])]
        
        return x_conv*self.get_scale()
       
    
    def set_axis_status(self, ax = None, status = "off"):
        """ Turn on or off the axis in 2d plot (x axis or y axis)
        
        ax: matplotlib.axes._subplots.AxesSubplot
        status: "off" or "on"
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        ax.axis(status)
    
    
    def set_axis_ticks_BL(self, ax = None, tick_rotation = 0, tick_interval = 0.1, tick_length = 0.015, **plt_kwargs):
        """ Plotting ticks in left and bottom axis in ternary diagram, assume tickers are uniform distributed in axis
        
        ax: matplotlib.axes._subplots.AxesSubplot
        tick_rotation: in degree
        tick_interval: interval between the ticks in axis.
        tick_length: the length of ticks
        plt_kwargs: a dict contains the options for plotting ticks.
        
        Returns: does not return anything.
        """
        
        if int(self.get_scale() / tick_interval) != self.get_scale() / tick_interval:
            raise ValueError("Ticker interval divided by scale is not an integer")
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        
        if "linewidth" not in plt_kwargs.keys():
            plt_kwargs["linewidth"] = 1
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = "k"
        
        tick_length *= self.get_scale()
        interval_num = int(self.get_scale()/tick_interval) + 1
        tick_pos = np.linspace(0, self.get_scale(), interval_num)
        tick_rotation = np.pi * tick_rotation / 180
        
        tick_xy_bottom = [np.cos(tick_rotation - np.pi/2)*tick_length, np.sin(tick_rotation - np.pi/2)*tick_length]
#        tick_xy_right = [np.cos(np.pi/6 + tick_rotation)*tick_length, np.sin(np.pi/6 + tick_rotation)*tick_length]
        tick_xy_left = [np.cos(5/6*np.pi + tick_rotation)*tick_length, np.sin(5/6*np.pi + tick_rotation)*tick_length]
        
        tick_pos_bottomstart =  [[i, 0] for i in tick_pos]
        tick_pos_bottomstop = [[i + tick_xy_bottom[0], tick_xy_bottom[1]] for i in tick_pos]
        
#        tick_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos]
#        tick_pos_rightstop = [[tick_pos_rightstart[j][0] + tick_xy_right[0], tick_pos_rightstart[j][1] + tick_xy_right[1]] for j in range(interval_num)]
        
        tick_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos]
        tick_pos_leftstop = [[tick_pos_leftstart[j][0] + tick_xy_left[0], tick_pos_leftstart[j][1] + tick_xy_left[1]] for j in range(interval_num)]
        
        for j in range(interval_num):
            ax.plot([tick_pos_bottomstart[j][0], tick_pos_bottomstop[j][0]], [tick_pos_bottomstart[j][1], tick_pos_bottomstop[j][1]], label = "", **plt_kwargs)
#            ax.plot([tick_pos_rightstart[j][0], tick_pos_rightstop[j][0]], [tick_pos_rightstart[j][1], tick_pos_rightstop[j][1]], color = "k")
            ax.plot([tick_pos_leftstart[j][0], tick_pos_leftstop[j][0]], [tick_pos_leftstart[j][1], tick_pos_leftstop[j][1]], label = "", **plt_kwargs)
    
    
    def set_axis_ticks_BRL(self, ax = None, tick_rotation = 0, tick_interval = 0.1, tick_length = 0.015, **plt_kwargs):
        """ Plotting ticks in three axis in ternary diagram, assume tickers are uniform distributed in axis
        
        ax: matplotlib.axes._subplots.AxesSubplot
        tick_rotation: in degree
        tick_interval: interval between the ticks in axis.
        tick_length: the length of ticks
        plt_kwargs: a dict contains the options for plotting ticks.
        
        Returns: does not return anything.
        """
        
        if int(self.get_scale() / tick_interval) != self.get_scale() / tick_interval:
            raise ValueError("Ticker interval divided by scale is not an integer")
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        
        if "linewidth" not in plt_kwargs.keys():
            plt_kwargs["linewidth"] = 1
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = "k"
        
        tick_length *= self.get_scale()
        interval_num = int(self.get_scale()/tick_interval) + 1
        tick_pos = np.linspace(0, self.get_scale(), interval_num)
        tick_rotation = np.pi * tick_rotation / 180
        
        tick_xy_bottom = [np.cos(tick_rotation - np.pi/2)*tick_length, np.sin(tick_rotation - np.pi/2)*tick_length]
        tick_xy_right = [np.cos(np.pi/6 + tick_rotation)*tick_length, np.sin(np.pi/6 + tick_rotation)*tick_length]
        tick_xy_left = [np.cos(5/6*np.pi + tick_rotation)*tick_length, np.sin(5/6*np.pi + tick_rotation)*tick_length]
        
        tick_pos_bottomstart =  [[i, 0] for i in tick_pos]
        tick_pos_bottomstop = [[i + tick_xy_bottom[0], tick_xy_bottom[1]] for i in tick_pos]
        
        tick_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos]
        tick_pos_rightstop = [[tick_pos_rightstart[j][0] + tick_xy_right[0], tick_pos_rightstart[j][1] + tick_xy_right[1]] for j in range(interval_num)]
        
        tick_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos]
        tick_pos_leftstop = [[tick_pos_leftstart[j][0] + tick_xy_left[0], tick_pos_leftstart[j][1] + tick_xy_left[1]] for j in range(interval_num)]
        
#        tick_pos_startall = tick_pos_bottomstart + tick_pos_rightstart + tick_pos_leftstart
#        tick_pos_stopall = tick_pos_bottomstop + tick_pos_rightstop + tick_pos_leftstop
        
        for j in range(interval_num):
            ax.plot([tick_pos_bottomstart[j][0], tick_pos_bottomstop[j][0]], [tick_pos_bottomstart[j][1], tick_pos_bottomstop[j][1]], label = "", **plt_kwargs)
            ax.plot([tick_pos_rightstart[j][0], tick_pos_rightstop[j][0]], [tick_pos_rightstart[j][1], tick_pos_rightstop[j][1]], label = "", **plt_kwargs)
            ax.plot([tick_pos_leftstart[j][0], tick_pos_leftstop[j][0]], [tick_pos_leftstart[j][1], tick_pos_leftstop[j][1]], label = "", **plt_kwargs)


    def set_ticks_label_BL(self, ax = None, label_rotation = 0, tick_interval = 0.1, offdis = 0.05, fontsize = 14, txt_kwargs = {}):
        """ add ticks labels in left and bottom axis in ternary diagram, assume tickers are uniform distributed in axis
        
        ax: matplotlib.axes._subplots.AxesSubplot
        label_rotation: a number in degree or a 1 dimensional matrix or list with 2 number for bottom label rotation and left label rotation
        tick_interval: interval between the ticks in axis.
        offdis: the distance from axis to the center of labels, offdis*scale is the real distance. This is affected to tick_length.
        txt_kwargs: a dict contains the options for labels.
        
        Returns: does not return anything.
        """
        
        if int(self.get_scale() / tick_interval) != self.get_scale() / tick_interval:
            raise ValueError("Ticker interval divided by scale is not an integer")
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        
        offdis *= self.get_scale()
        interval_num = int(self.get_scale()/tick_interval) + 1
        
        round_number = len(str(tick_interval-int(tick_interval))) - 2
        if round_number >= 1:
            tick_pos = [round(i*tick_interval, round_number) for i in range(interval_num)]
        else:
            tick_pos = [i*tick_interval for i in range(interval_num)]

        label_xy_bottom = [np.cos(-np.pi/2) * offdis, np.sin(-np.pi/2) * offdis]
#        label_xy_right = [np.cos(np.pi/6) * offdis, np.sin(np.pi/6) * offdis]
        label_xy_left = [np.cos(5/6*np.pi) * offdis, np.sin(5/6*np.pi) * offdis]
        
#        label_pos_bottomstart =  [[i, 0] for i in tick_pos]
        label_pos_bottomstop = [[i + label_xy_bottom[0], label_xy_bottom[1]] for i in tick_pos]
        
#        label_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos]
#        label_pos_rightstop = [[label_pos_rightstart[j][0] + label_xy_right[0], label_pos_rightstart[j][1] + label_xy_right[1]] for j in range(interval_num)]
        
        label_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos]
        label_pos_leftstop = [[label_pos_leftstart[j][0] + label_xy_left[0], label_pos_leftstart[j][1] + label_xy_left[1]] for j in range(interval_num)]

#        vertex_coords = np.array([(0, 0), (1, 0), (1/2, np.sqrt(3)/2)])*self.get_scale()
#        if axis_range == None:
        if isinstance(label_rotation, list) or isinstance(label_rotation, np.ndarray):
            if len(label_rotation) == 2:
                label_bottom_rotation = label_rotation[0]
#                label_right_rotation = label_rotation[1]
                label_left_rotation = label_rotation[1]
            else:
                raise ValueError("a list or array must contain 3 values here")
        else:
            label_bottom_rotation = label_rotation
#            label_right_rotation = 30 + label_rotation
            label_left_rotation = -30 + label_rotation
        for j in range(interval_num):
            ax.text(label_pos_bottomstop[j][0], label_pos_bottomstop[j][1], str(tick_pos[j]), horizontalalignment='center',
                 verticalalignment='center', rotation = label_bottom_rotation, fontsize = fontsize, **txt_kwargs)
#            ax.text(label_pos_rightstop[j][0], label_pos_rightstop[j][1], str(tick_pos[j]), horizontalalignment='center',
#                 verticalalignment='center', rotation = label_right_rotation, fontsize = fontsize)
            ax.text(label_pos_leftstop[j][0], label_pos_leftstop[j][1], str(tick_pos[::-1][j]), horizontalalignment='center',
                 verticalalignment='center', rotation = label_left_rotation, fontsize = fontsize, **txt_kwargs)

    
    def set_ticks_label_BRL(self, ax = None, label_rotation = 0, tick_interval = 0.1, offdis = 0.05, fontsize = 14, txt_kwargs = {}):
        """ add ticks labels in three corners in ternary diagram, assume tickers are uniform distributed in axis
        
        ax: matplotlib.axes._subplots.AxesSubplot
        label_rotation: a number in degree or a 1 dimensional matrix or list with 2 number for bottom label rotation and left label rotation
        tick_interval: interval between the ticks in axis.
        offdis: the distance from axis to the center of labels, offdis*scale is the real distance. This is affected to tick_length.
        txt_kwargs: a dict contains the options for labels.
        
        Returns: does not return anything.
        """
        
        if int(self.get_scale() / tick_interval) != self.get_scale() / tick_interval:
            raise ValueError("Ticker interval divided by scale is not an integer")
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        
        offdis *= self.get_scale()
        interval_num = int(self.get_scale()/tick_interval) + 1
        
        round_number = len(str(tick_interval-int(tick_interval))) - 2
        if round_number >= 1:
            tick_pos = [round(i*tick_interval, round_number) for i in range(interval_num)]
        else:
            tick_pos = [i*tick_interval for i in range(interval_num)]

        label_xy_bottom = [np.cos(-np.pi/2) * offdis, np.sin(-np.pi/2) * offdis]
        label_xy_right = [np.cos(np.pi/6) * offdis, np.sin(np.pi/6 ) * offdis]
        label_xy_left = [np.cos(5/6*np.pi) * offdis, np.sin(5/6*np.pi) * offdis]
        
#        label_pos_bottomstart =  [[i, 0] for i in tick_pos]
        label_pos_bottomstop = [[i + label_xy_bottom[0], label_xy_bottom[1]] for i in tick_pos]
        
        label_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos]
        label_pos_rightstop = [[label_pos_rightstart[j][0] + label_xy_right[0], label_pos_rightstart[j][1] + label_xy_right[1]] for j in range(interval_num)]
        
        label_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos]
        label_pos_leftstop = [[label_pos_leftstart[j][0] + label_xy_left[0], label_pos_leftstart[j][1] + label_xy_left[1]] for j in range(interval_num)]

        if isinstance(label_rotation, list) or isinstance(label_rotation, np.ndarray):
            if len(label_rotation) == 3:
                label_bottom_rotation = label_rotation[0]
                label_right_rotation = label_rotation[1]
                label_left_rotation = label_rotation[2]
            else:
                raise ValueError("a list or array must contain 3 values here")
        else:
            label_bottom_rotation = label_rotation
            label_right_rotation = 30 + label_rotation
            label_left_rotation = -30 + label_rotation
        for j in range(interval_num):
            ax.text(label_pos_bottomstop[j][0], label_pos_bottomstop[j][1], str(tick_pos[j]), horizontalalignment='center',
                 verticalalignment='center', rotation = label_bottom_rotation, fontsize = fontsize, **txt_kwargs)
            ax.text(label_pos_rightstop[j][0], label_pos_rightstop[j][1], str(tick_pos[j]), horizontalalignment='center',
                 verticalalignment='center', rotation = label_right_rotation, fontsize = fontsize, **txt_kwargs)
            ax.text(label_pos_leftstop[j][0], label_pos_leftstop[j][1], str(tick_pos[j]), horizontalalignment='center',
                 verticalalignment='center', rotation = label_left_rotation, fontsize = fontsize, **txt_kwargs)

    
    def set_zoomin_axis_ticks_bilateral(self, ax = None, startpoint = "left", tick_rotation = 0, tick_interval = 0.1, tick_length = 0.015, plt_kwargs = {}):
        """ add ticks in two axes in zoomin ternary diagram, assume tickers are uniform distributed in axis
        
        ax: matplotlib.axes._subplots.AxesSubplot
        startpoint: the label of corner point where the angle between its two near length sides is 60 degree.  
        tick_rotation: a number in degree
        tick_interval: interval between the ticks in axis.
        tick_length: the length of ticks.
        plt_kwargs: a dict contains the options for labels.
        
        Returns: does not return anything.
        """
        
        if int(self.get_scale() / tick_interval) != self.get_scale() / tick_interval:
            raise ValueError("Ticker interval divided by scale is not an integer")
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "color" not in plt_kwargs.keys():
            plt_kwargs["color"] = "k"
            
        tick_length *= self.get_scale()
        interval_num = int(self.get_scale()/tick_interval) + 1
        tick_pos = np.linspace(0, self.get_scale(), interval_num)
        tick_rotation = np.pi * tick_rotation / 180
        
        tick_xy_bottom = [np.cos(tick_rotation - np.pi/2)*tick_length, np.sin(tick_rotation - np.pi/2)*tick_length]
        tick_xy_right = [np.cos(np.pi/6 + tick_rotation)*tick_length, np.sin(np.pi/6 + tick_rotation)*tick_length]
        tick_xy_left = [np.cos(5/6*np.pi + tick_rotation)*tick_length, np.sin(5/6*np.pi + tick_rotation)*tick_length]
        
        tick_pos_bottomstart =  [[i, 0] for i in tick_pos]
        tick_pos_bottomstop = [[i + tick_xy_bottom[0], tick_xy_bottom[1]] for i in tick_pos]
        
        tick_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos]
        tick_pos_rightstop = [[tick_pos_rightstart[j][0] + tick_xy_right[0], tick_pos_rightstart[j][1] + tick_xy_right[1]] for j in range(interval_num)]
        
        tick_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos]
        tick_pos_leftstop = [[tick_pos_leftstart[j][0] + tick_xy_left[0], tick_pos_leftstart[j][1] + tick_xy_left[1]] for j in range(interval_num)]
        
        if startpoint == "top":
            for j in range(interval_num):
#                ax.plot([tick_pos_bottomstart[j][0], tick_pos_bottomstop[j][0]], [tick_pos_bottomstart[j][1], tick_pos_bottomstop[j][1]], **plt_kwargs)
                ax.plot([tick_pos_rightstart[j][0], tick_pos_rightstop[j][0]], [tick_pos_rightstart[j][1], tick_pos_rightstop[j][1]], **plt_kwargs)
                ax.plot([tick_pos_leftstart[j][0], tick_pos_leftstop[j][0]], [tick_pos_leftstart[j][1], tick_pos_leftstop[j][1]], **plt_kwargs)
        elif startpoint == "left":
            for j in range(interval_num):
                ax.plot([tick_pos_bottomstart[j][0], tick_pos_bottomstop[j][0]], [tick_pos_bottomstart[j][1], tick_pos_bottomstop[j][1]], **plt_kwargs)
    #            ax.plot([tick_pos_rightstart[j][0], tick_pos_rightstop[j][0]], [tick_pos_rightstart[j][1], tick_pos_rightstop[j][1]], color = "k")
                ax.plot([tick_pos_leftstart[j][0], tick_pos_leftstop[j][0]], [tick_pos_leftstart[j][1], tick_pos_leftstop[j][1]], **plt_kwargs)
        elif startpoint == "right":
            for j in range(interval_num):
                ax.plot([tick_pos_bottomstart[j][0], tick_pos_bottomstop[j][0]], [tick_pos_bottomstart[j][1], tick_pos_bottomstop[j][1]], **plt_kwargs)
                ax.plot([tick_pos_rightstart[j][0], tick_pos_rightstop[j][0]], [tick_pos_rightstart[j][1], tick_pos_rightstop[j][1]], **plt_kwargs)
#                ax.plot([tick_pos_leftstart[j][0], tick_pos_leftstop[j][0]], [tick_pos_leftstart[j][1], tick_pos_leftstop[j][1]], **plt_kwargs)
        else:
            raise ValueError("startpoint is not in ['top', 'left', 'right']")
    
    def set_zoomin_ticks_label_bilateral(self, axis_range = [], ax = None, startpoint = "left", label_rotation = 0, tick_interval = 0.1, offdis = 0.05, fontsize = 10, txt_kwargs = {}):
        """ add ticks labels in two axes in zoomin ternary diagram, assume tickers are uniform distributed in axis
        
        ax: matplotlib.axes._subplots.AxesSubplot
        startpoint: the label of corner point where the angle between its two near sides is 60 degree. The tick labels will
            be add along these two sides.
        tick_rotation: a number in degree
        tick_interval: interval between the ticks in axis.
        tick_length: the length of ticks.
        txt_kwargs: a dict contains the options for labels.
        
        Returns: does not return anything.
        """
        
        if len(axis_range) == 0:
            raise ValueError("axisrange cannot be empty")
        for item in axis_range:
            if sum(item)/self.get_scale() != 1:
                raise ValueError("the sum of coordinates of one point not equal to 1")
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)

        offdis *= self.get_scale()
        label_xy_bottom = [np.cos(-np.pi/2) * offdis, np.sin(-np.pi/2) * offdis]
        label_xy_right = [np.cos(np.pi/6) * offdis, np.sin(np.pi/6) * offdis]
        label_xy_left = [np.cos(5/6*np.pi) * offdis, np.sin(5/6*np.pi) * offdis]
        
        if isinstance(label_rotation, list) or isinstance(label_rotation, np.ndarray):
            if len(label_rotation) == 3:
                label_bottom_rotation = label_rotation[0]
                label_right_rotation = label_rotation[1]
                label_left_rotation = label_rotation[2]
            else:
                raise ValueError("a list or array must contain 3 values here")
        else:
            label_bottom_rotation = label_rotation
            label_right_rotation = 30 + label_rotation
            label_left_rotation = -30 + label_rotation
            
        interval_num = int(self.get_scale()/tick_interval) + 1
        tick_pos = [i*tick_interval for i in range(interval_num)]
        
        bottom_interval = (Decimal(str(axis_range[1][1])) - Decimal(str(axis_range[0][1])))/(interval_num-1)
        right_interval = (Decimal(str(axis_range[2][2])) - Decimal(str(axis_range[1][2])))/(interval_num-1)
        left_interval = (Decimal(str(axis_range[0][0])) - Decimal(str(axis_range[1][0])))/(interval_num-1)
        
        tick_pos_bottomstr = [Decimal(str(axis_range[0][1])) + i*bottom_interval for i in range(interval_num)]
        tick_pos_rightstr = [Decimal(str(axis_range[1][2])) + i*right_interval for i in range(interval_num)]
        tick_pos_leftstr = [Decimal(str(axis_range[2][0])) + i*left_interval for i in range(interval_num)]
        
#            label_pos_bottomstart =  [[i, 0] for i in tick_pos]
        label_pos_bottomstop = [[i + label_xy_bottom[0], label_xy_bottom[1]] for i in tick_pos]
        
        label_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos]
        label_pos_rightstop = [[label_pos_rightstart[j][0] + label_xy_right[0], label_pos_rightstart[j][1] + label_xy_right[1]] for j in range(interval_num)]
        
        label_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos]
        label_pos_leftstop = [[label_pos_leftstart[j][0] + label_xy_left[0], label_pos_leftstart[j][1] + label_xy_left[1]] for j in range(interval_num)]
        
        if startpoint == "top":
            tick_pos_rightstr = tick_pos_bottomstr[::-1]
            for j in range(interval_num):
                ax.text(label_pos_rightstop[j][0], label_pos_rightstop[j][1], tick_pos_rightstr[j], horizontalalignment='center',
                     verticalalignment='center', rotation = label_right_rotation, fontsize = fontsize, **txt_kwargs)
                ax.text(label_pos_leftstop[j][0], label_pos_leftstop[j][1], tick_pos_leftstr[j], horizontalalignment='center',
                     verticalalignment='center', rotation = label_left_rotation, fontsize = fontsize, **txt_kwargs)
        elif startpoint == "left":
            tick_pos_leftstr = tick_pos_rightstr[::-1]
            for j in range(interval_num):
                ax.text(label_pos_bottomstop[j][0], label_pos_bottomstop[j][1], tick_pos_bottomstr[j], horizontalalignment='center',
                     verticalalignment='center', rotation = label_bottom_rotation, fontsize = fontsize, **txt_kwargs)
                ax.text(label_pos_leftstop[j][0], label_pos_leftstop[j][1], tick_pos_leftstr[j], horizontalalignment='center',
                     verticalalignment='center', rotation = label_left_rotation, fontsize = fontsize, **txt_kwargs)
        elif startpoint == "right":
            tick_pos_bottomstr = tick_pos_leftstr[::-1]
            for j in range(interval_num):
                ax.text(label_pos_bottomstop[j][0], label_pos_bottomstop[j][1], tick_pos_bottomstr[j], horizontalalignment='center',
                     verticalalignment='center', rotation = label_bottom_rotation, fontsize = fontsize, **txt_kwargs)
                ax.text(label_pos_rightstop[j][0], label_pos_rightstop[j][1], tick_pos_rightstr[j], horizontalalignment='center',
                     verticalalignment='center', rotation = label_right_rotation, fontsize = fontsize, **txt_kwargs)
        else:
            raise ValueError("startpoint is not in ['top', 'left', 'right']")
#        else:
#            bottom_interval = real_interval[0]
#            right_interval = real_interval[1]
#            left_interval = real_interval[2]
#            
#            interval_num_bottom = int ((Decimal(str(axis_range[1][1])) - Decimal(str(axis_range[0][1]))) / Decimal(str(bottom_interval)))
#            interval_num_right = int ((Decimal(str(axis_range[2][2])) - Decimal(str(axis_range[1][2]))) / Decimal(str(right_interval)))
#            interval_num_left = int ((Decimal(str(axis_range[0][0])) - Decimal(str(axis_range[1][0]))) / Decimal(str(left_interval)))
#            
#            tick_pos_bottomstr = [Decimal(str(axis_range[0][1])) + i*Decimal(str(bottom_interval)) for i in range(interval_num_bottom)]
#            tick_pos_rightstr = [Decimal(str(axis_range[1][2])) + i*Decimal(str(right_interval)) for i in range(interval_num_right)]
#            tick_pos_leftstr = [Decimal(str(axis_range[2][0])) + i*Decimal(str(left_interval)) for i in range(interval_num_left)]
#            
#            tick_pos_bottom = [i*bottom_interval for i in range(interval_num_bottom)]
#            tick_pos_right = [i*right_interval for i in range(interval_num_right)]
#            tick_pos_left = [i*left_interval for i in range(interval_num_left)]
##            label_pos_bottomstart =  [[i, 0] for i in tick_pos]
#            label_pos_bottomstop = [[i + label_xy_bottom[0], label_xy_bottom[1]] for i in tick_pos_bottom]
#            
#            label_pos_rightstart = [[self.get_scale() - 0.5*j, j*np.sqrt(3)/2] for j in tick_pos_right]
#            label_pos_rightstop = [[label_pos_rightstart[j][0] + label_xy_right[0], label_pos_rightstart[j][1] + label_xy_right[1]] for j in range(interval_num_right)]
#            
#            label_pos_leftstart = [[self.get_scale()/2 - j*0.5, np.sqrt(3)/2*self.get_scale() - j*np.sqrt(3)/2] for j in tick_pos_left]
#            label_pos_leftstop = [[label_pos_leftstart[j][0] + label_xy_left[0], label_pos_leftstart[j][1] + label_xy_left[1]] for j in range(interval_num_left)]
#            
#            if startpoint == "top":
#                tick_pos_rightstr = tick_pos_bottomstr[::-1]
#                for j in range(interval_num_right):
#                    ax.text(label_pos_rightstop[j][0], label_pos_rightstop[j][1], tick_pos_rightstr[j], horizontalalignment='center',
#                         verticalalignment='center', rotation = label_right_rotation, fontsize = fontsize)
#                for j in range(interval_num_left):
#                    ax.text(label_pos_leftstop[j][0], label_pos_leftstop[j][1], tick_pos_leftstr[j], horizontalalignment='center',
#                         verticalalignment='center', rotation = label_left_rotation, fontsize = fontsize)
#            elif startpoint == "left":
#                tick_pos_leftstr = tick_pos_rightstr[::-1]
#                for j in range(interval_num_bottom):
#                    ax.text(label_pos_bottomstop[j][0], label_pos_bottomstop[j][1], tick_pos_bottomstr[j], horizontalalignment='center',
#                         verticalalignment='center', rotation = label_bottom_rotation, fontsize = fontsize)
#                for j in range(interval_num_left):
#                    ax.text(label_pos_leftstop[j][0], label_pos_leftstop[j][1], tick_pos_leftstr[j], horizontalalignment='center',
#                         verticalalignment='center', rotation = label_left_rotation, fontsize = fontsize)
#            elif startpoint == "right":
#                tick_pos_bottomstr = tick_pos_leftstr[::-1]
#                for j in range(interval_num_bottom):
#                    ax.text(label_pos_bottomstop[j][0], label_pos_bottomstop[j][1], tick_pos_bottomstr[j], horizontalalignment='center',
#                         verticalalignment='center', rotation = label_bottom_rotation, fontsize = fontsize)
#                for j in range(interval_num_right):
#                    ax.text(label_pos_rightstop[j][0], label_pos_rightstop[j][1], tick_pos_rightstr[j], horizontalalignment='center',
#                         verticalalignment='center', rotation = label_right_rotation, fontsize = fontsize)        
            
    
    def set_left_corner_label(self, ax = None, label = "left corner", offdis = 0.08, rotation = 0, txt_kwargs = {}):
        """ To add the left coner label
        
        label: a string of content to add
        offdis: the distance to the corner vertex, offdis*scale is the real distance
        rotation: the degree to rotate
        txt_kwargs: a dict contains the options for the label.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "fontsize" not in txt_kwargs.keys():
            txt_kwargs["fontsize"] = 16
        
        x, y = [-offdis*self.scale, -1/3*offdis*self.scale]
        ax.text(x, y, label, horizontalalignment='center',
                 verticalalignment='center', rotation = rotation, **txt_kwargs)
        
    
    def set_right_corner_label(self, ax = None, label = "right corner", offdis = 0.08, rotation = 0, txt_kwargs = {}):
        """ To add the right coner label
        
        label: a string of content to add
        offdis: the distance to the corner vertex, offdis*scale is the real distance
        rotation: the degree to rotate
        txt_kwargs: a dict contains the options for the label.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "fontsize" not in txt_kwargs.keys():
            txt_kwargs["fontsize"] = 16
        
        x, y = [self.scale + offdis*self.scale, -1/3*offdis*self.scale]
        ax.text(x, y, label, horizontalalignment='center',
                 verticalalignment='center', rotation = rotation, **txt_kwargs)
    
    
    def set_top_corner_label(self, ax = None, label = "top corner", offdis = 0.08, rotation = 0, txt_kwargs = {}):
        """ To add the top coner label
        
        label: a string of content to add
        offdis: the distance to the corner vertex, offdis*scale is the real distance
        rotation: the degree to rotate
        txt_kwargs: a dict contains the options for the label.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "fontsize" not in txt_kwargs.keys():
            txt_kwargs["fontsize"] = 16

        x, y = [0.5 * self.scale, np.sqrt(3)/2 * (self.scale + offdis*self.scale)]
        ax.text(x, y, label, horizontalalignment='center',
                 verticalalignment='center', rotation = rotation, **txt_kwargs)
        
    
    def set_bottom_axis_label(self, ax = None, label = "bottom axis", offdis = 0.05, rotation = 0, txt_kwargs = {}):
        """ To add the bottom axis label
        
        label: a string of content to add
        offdis: the distance to the corner vertex, offdis*scale is the real distance
        rotation: the degree to rotate
        txt_kwargs: a dict contains the options for the label.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "fontsize" not in txt_kwargs.keys():
            txt_kwargs["fontsize"] = 16

        x, y = [0.5 * self.scale, -self.scale * offdis*2]
        ax.text(x, y, label, horizontalalignment='center',
                 verticalalignment='center', rotation = rotation, **txt_kwargs)        
    
    
    def set_right_axis_label(self, ax = None, label = "right axis", offdis = 0.05, rotation = 0, txt_kwargs = {}):
        """ To add the right axis label
        
        label: a string of content to add
        offdis: the distance to the corner vertex, offdis*scale is the real distance
        rotation: the degree to rotate
        txt_kwargs: a dict contains the options for the label.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "fontsize" not in txt_kwargs.keys():
            txt_kwargs["fontsize"] = 16
        
        offdis_y, offdis_x = [offdis*self.scale * 0.5 *2, offdis*self.scale * np.sqrt(3)/2 *2]
        x, y = [0.75 * self.scale + offdis_x, np.sqrt(3)/4 * self.scale + offdis_y]
        ax.text(x, y, label, horizontalalignment='center',
                 verticalalignment='center', rotation = rotation - 60, **txt_kwargs)
    
    
    def set_left_axis_label(self, ax = None, label = "left axis", offdis = 0.05, rotation = 0, txt_kwargs = {}):
        """ To add the left axis label
        
        label: a string of content to add
        offdis: the distance to the corner vertex, offdis*scale is the real distance
        rotation: the degree to rotate
        txt_kwargs: a dict contains the options for the label.
        
        Returns: does not return anything.
        """
        
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        if "fontsize" not in txt_kwargs.keys():
            txt_kwargs["fontsize"] = 16

        offdis_y, offdis_x = [offdis*self.scale * 0.5 *2, -offdis*self.scale * np.sqrt(3)/2 *2]
        x, y = [0.25 * self.scale + offdis_x, np.sqrt(3)/4 * self.scale + offdis_y]
        ax.text(x, y, label, horizontalalignment='center',
                 verticalalignment='center', rotation = rotation + 60, **txt_kwargs)
        

    def plot(self, x, ax = None, **plt_kwargs):
        """ Plotting 3d data in 2d ternary plot
        
        x: (n x 3) dimensional array or list
        ax: matplotlib.axes._subplots.AxesSubplot
        
        Returns: an legend handle
        """
        
        if x is None:
            return
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
    
        x_conv = self.coordinates_conversion(x)
#        ax.set_xlim([-0.1 * self.scale, 1.1 * self.scale])
#        ax.set_ylim([-0.1 * 2 / np.sqrt(3) *self.scale, 1.1 * 2 / np.sqrt(3) * self.scale])
    #    print(data_conv)
#        if not label:
#            plt_kwargs["label"] = label
        return ax.plot(x_conv[:, 0], x_conv[:, 1], **plt_kwargs)
    
    
    def show_legend(self, ax = None, **lg_kwargs):
        """ Add legend to plots
        
        ax: matplotlib.axes._subplots.AxesSubplot
        labels: labels for each group of data
        lg_kwargs: a dict of params for legend
        
        Returns: does not return anything.
        """
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, 8)
        ax.legend(**lg_kwargs)
