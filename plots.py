# -*- coding: utf-8 -*-
"""
Created on Tue Mar 23 16:02:07 2021

@author: ustcw
"""

from pyTernary.ternaryPlot import TernaryPlot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

#%% ternary_plot
def ternary_plot(tp, data, ax = None, interval = 0.1, tick_length = 0.015, tick_rotation = 0, label_rotation = 0, corner_labels = [], legend_status =False, savefig = False, fig_path = "", fig_name = "Phases data", **kwargs):
        """ Mapping 3d data points to the equilateral triangle region in 2d (ternary plot).
        
        tp: TernaryPlot object
        data: a list or array of data
        ax: matplotlib.axes._subplots.AxesSubplot
        interval: a number, the gridlines' interval
        
        Returns: does not return anything.
        """
        if "color" not in kwargs.keys():
            kwargs["color"] = "r"
        if "linewidth" not in kwargs.keys():
            kwargs["linewidth"] = 0
        if "marker" not in kwargs.keys():
            kwargs["marker"] = "."
        if ax == None:
            fig, ax = plt.subplots()
            fig.set_size_inches(8, np.sqrt(3)/2*8)
            
        tp.set_boundary(ax)
        tp.set_gridlines(ax, interval = interval)
        
        tp.set_axis_status(ax, status = "off")
        tp.set_axis_ticks_BRL(ax, tick_rotation = 0, tick_interval = interval, tick_length = tick_length)
        tp.set_ticks_label_BRL(ax, label_rotation = 0, tick_interval = interval, offdis = 3*tick_length, fontsize= 12)
        if corner_labels:
            tp.set_left_corner_label(ax, corner_labels[0])
            tp.set_right_corner_label(ax, corner_labels[1])
            tp.set_top_corner_label(ax, corner_labels[2])
        
        tp.plot(data, ax, **kwargs)
        if legend_status:
            ax.legend()
        if savefig:
                fig.savefig(fig_path + "{}.png".format(fig_name))


#%% plotting data for tie lines 

def tielines_plot(data, columns = [], colors = [], markers = [], components = [], scale = 1, interval = 0.1, tick_length = 0.015, add_marker = True, legend_status = True, title_status = False, savefig = False, fig_path = "", fig_name = "Tie-lines data", mode = 2, **kwargs):
    """
    data: a DataFrame of tielines data with designed columns
    columns: a list of two columns names to be classified, the first column is about temperature, the second one is about reference.
    colors: a list of colors
    markers: a list of markers
    components: a list of ternary elements.
    legend_status: true for showing legend
    save_fig: true for saving figure
    fig_path: when save_fig is true, save the figure in desired file; if false, save the figure in current file
    fig_name: the main body of the saved figures
    """
    if "linewidth" not in kwargs.keys():
        kwargs["linewidth"] = 1

    if not components:
        if "Components" in data.columns:
            components = list(data["Components"].dropna())
        else:
            raise ValueError("The Components is not in the DataFrame and is not defined.")
    elif len(components) != 3:
        raise ValueError("The dimension of components is not equal to 3.")
    if "Phase 3" in data.columns:
        all_comps = np.array([[components[i] + "_" + str(j) for i in range(0,3)] for j in range(1,4)])
        comp11, comp12, comp13 = components[0] + "_1", components[1] + "_1", components[2] + "_1"
        comp21, comp22, comp23 = components[0] + "_2", components[1] + "_2", components[2] + "_2"
        comp31, comp32, comp33 = components[0] + "_3", components[1] + "_3", components[2] + "_3"
        Phase3_in_column = True
    else:
        all_comps = np.array([[components[i] + "_" + str(j) for i in range(0,2)] for j in range(1,3)])
        comp11, comp12, comp13 = components[0] + "_1", components[1] + "_1", components[2] + "_1"
        comp21, comp22, comp23 = components[0] + "_2", components[1] + "_2", components[2] + "_2"
        Phase3_in_column = False
    for comp in all_comps.ravel():
        if comp not in data.columns:
            raise ValueError("The {} is not in the DataFrame.".format(comp))
    
    if mode == 1:
        if not columns:
            column1, column2 = ["T/K", "Ref"]
        else:
            column1, column2 = columns
        if not colors:
            colors = ["r", "g", "b", "orange", "black", "cyan", "purple"]
        if not markers:
            markers = ["o", "d",  "s", "p", "x", "D", "P", "*",]
        if column1 == "T/K":
            string = "K"
        else:
            string = ""
        
        group_tielines_T = data.groupby(by = [column1])
        for key in group_tielines_T.groups.keys():
            tp = TernaryPlot(scale = scale)
            fig, ax = plt.subplots()
            fig.set_size_inches(8, np.sqrt(3)/2*8)
            
            tp.set_boundary(ax = ax)
            tp.set_gridlines(ax = ax, interval = interval)
            tp.set_axis_status(ax, status = "off")
            tp.set_axis_ticks_BRL(ax, tick_rotation = 0, tick_interval = interval, tick_length = tick_length)
            tp.set_ticks_label_BRL(ax, label_rotation = 0, tick_interval = interval, offdis = 4*tick_length)
            # set corner labels
            tp.set_left_corner_label(ax, label = components[0], offdis = 6*tick_length, rotation = 0)
            tp.set_right_corner_label(ax, label = components[1], offdis = 6*tick_length, rotation = 0)
            tp.set_top_corner_label(ax, label = components[2], offdis = 6*tick_length, rotation = 0)
            group_tielines_Tref = group_tielines_T.get_group(key).groupby(by = [column2])
            
            for j, key1 in enumerate(group_tielines_Tref.groups.keys()):
                rows = group_tielines_Tref.get_group(key1)
#                rows.sort_values(by=['Ref'])
                for idex in range(len(rows)):
                    data_row = rows.iloc[idex]
                    if Phase3_in_column:
                        if pd.isna(data_row["Phase 3"]):
                            tieline_points = [data_row[[comp11, comp12, comp13]], 
                                                       data_row[[comp21, comp22, comp23]]]
                        else:
                            tieline_points = [data_row[[comp11, comp12, comp13]],
                                               data_row[[comp21, comp22, comp23]],
                                               data_row[[comp31, comp32, comp33]],
                                               data_row[[comp11, comp12, comp13]],]
                        tp.plot(tieline_points, ax, color = colors[j], marker = markers[j], label = key1, **kwargs)
                    else:
                        tieline_points = [data_row[[comp11, comp12, comp13]], 
                                                       data_row[[comp21, comp22, comp23]]]
                        tp.plot(tieline_points, ax, color = colors[j], marker = markers[j], label = key1, **kwargs)
    
            if title_status:
                plt.suptitle("{} - {}{}".format(fig_name, key, string), fontsize = 16)
            if legend_status:
                handles, labels = plt.gca().get_legend_handles_labels()
                by_label = dict(zip(labels, handles))
                plt.legend(by_label.values(), by_label.keys())
            if savefig:
                fig.savefig(fig_path + "{} - {}{}.png".format(fig_name, key, string))
    
    elif mode == 2:
        if not columns:
            column1, style, hue = ["T/K", "Phase", "Ref"]
        else:
            column1, style, hue = columns
        if column1 == "T/K":
            string = "K"
        else:
            string = ""
        columns_name = [style] + components + [hue]  # this is for creating the dataframe
        group_tielines_T = data.groupby(by = [column1])
        for key in group_tielines_T.groups.keys():
            tp = TernaryPlot(scale = scale)
            fig, ax = plt.subplots()
            fig.set_size_inches(8, np.sqrt(3)/2*8)
            
            tp.set_boundary(ax = ax)
            tp.set_gridlines(ax = ax, interval = interval)
            tp.set_axis_status(ax, status = "off")
            tp.set_axis_ticks_BRL(ax, tick_rotation = 0, tick_interval = interval, tick_length = tick_length)
            tp.set_ticks_label_BRL(ax, label_rotation = 0, tick_interval = interval, offdis = 3.5*tick_length)
            # set corner labels
            tp.set_left_corner_label(ax, label = components[0], offdis = 6*tick_length, rotation = 0)
            tp.set_right_corner_label(ax, label = components[1], offdis = 6*tick_length, rotation = 0)
            tp.set_top_corner_label(ax, label = components[2], offdis = 6*tick_length, rotation = 0)
            
            rows = group_tielines_T.get_group(key)
            for idex in range(len(rows)):
                data_row = rows.iloc[idex]
                if Phase3_in_column:
                    if pd.isna(data_row["Phase 3"]):
                        tieline_points = [data_row[[comp11, comp12, comp13]], 
                                                   data_row[[comp21, comp22, comp23]]]                        
                    else:
                        tieline_points = [data_row[[comp11, comp12, comp13]],
                                           data_row[[comp21, comp22, comp23]],
                                           data_row[[comp31, comp32, comp33]],
                                           data_row[[comp11, comp12, comp13]],]
                    tp.plot(tieline_points, ax, color = "k", label = "", **kwargs)
                else:
                    tieline_points = [data_row[[comp11, comp12, comp13]], 
                                                   data_row[[comp21, comp22, comp23]]]
                    tp.plot(tieline_points, ax, color = "k", label = "", **kwargs)
            if Phase3_in_column:
                if rows[["Phase 3"]].dropna(how = "any").empty:
                    phase_data = np.concatenate([ np.array(rows[["Phase 1", comp11, comp12, comp13, hue]]),
                                           np.array(rows[["Phase 2", comp21, comp22, comp23, hue]]) ])
                else:
                    phase_data = np.concatenate([np.array(rows[["Phase 1", comp11, comp12, comp13, hue]]),
                          np.array(rows[["Phase 2", comp21, comp22, comp23, hue]]),
                          np.array(rows[["Phase 3", comp31, comp32, comp33, hue]].dropna(how = "any"))])
            else:
                phase_data = np.concatenate([ np.array(rows[["Phase 1", comp11, comp12, comp13, hue]]),
                                           np.array(rows[["Phase 2", comp21, comp22, comp23, hue]]) ])
            phases_data = pd.DataFrame(phase_data, columns = columns_name)
            markercolor_plot(phases_data, ax = ax, style = style, hue = hue, colors = colors, markers = markers, components = components, scale = scale, legend_status = legend_status, **kwargs)
            if title_status:
                plt.suptitle("{} - {}{}".format(fig_name, key, string), fontsize = 16)
            if savefig:
                fig.savefig(fig_path + "{} - {}{}.png".format(fig_name, key, string))
                
            

def markercolor_plot(data, ax = None, style = "Phase", hue = "Ref", colors = [], markers = [], components = [], scale = 1, legend_status = True, title_status = False, savefig = False, fig_path = "", fig_name = "Tie-lines data", **kwargs):
    """
    data: a DataFrame of tielines data with designed columns
    style: the labels denoted by different markers edged by black color
    hue: the labels denoted by circles with different colors 
    colors: a list of colors
    markers: a list of markers
    components: a list of ternary elements. The length is 3 for ternary plot (x,y,z), the length is 2 for regular plot (x, y).
    legend_status: true for showing legend
    save_fig: true for saving figure
    fig_path: when save_fig is true, save the figure in desired file; if false, save the figure in current file
    fig_name: the name of the saved figure
    """
    
    if not markers:
        markers = ["o", "D",  "s", "P", "X", "d", "p", "x", "+", "*", "^", "v", "<", ">", "H", "h", "1", "2", "3", "4"]
#        markers = ["o", "d",  "s", "p", "x", "D", "P", "*",]
    if not colors:
        cmap = matplotlib.cm.get_cmap('tab20')
        colors = [cmap(i) for i in np.linspace(0, 1, len(markers))]
        colors = colors[0::2] + colors[1::2]
#        colors = ["r", "g", "b", "orange", "black", "cyan", "purple"]
    if "linestyle" in kwargs.keys():
        kwargs.pop("linestyle")

#    if column1 == "T/K":
#        string = "K"
#    else:
#        string = ""
    
    if not components:
        if "Components" in data.columns:
            components = data["Components"].dropna()
        else:
            raise ValueError("The Components is not in the DataFrame and is not defined.")
    elif len(components) != 3:
        raise ValueError("The dimension of components is not equal to 3.")
            
    tp = TernaryPlot(scale = scale)
    if ax == None:
        fig, ax = plt.subplots()
        fig.set_size_inches(8, np.sqrt(3)/2*8)
    
    data = data.sort_values(by=[style, hue])
    style_unique = data[style].unique()
    styles = dict(zip(style_unique, range(len(style_unique))) )
    hue_unique = data[hue].unique()
    hues = dict( zip(hue_unique, range(len(hue_unique))) )

    group_phases_refs = data.groupby(by = [style, hue])
    if len(components) == 3:
        for key in group_phases_refs.groups.keys():
            marker = markers[styles[key[0]] ]
            color = colors[hues[key[1]]]
            tieline_points = np.array(group_phases_refs.get_group(key)[components])
            tp.plot(tieline_points, ax, color = color, marker = marker, ls="none", label = "", **kwargs)
    elif len(components) == 2:
        for key in group_phases_refs.groups.keys():
            marker = markers[styles[key[0]] ]
            color = colors[hues[key[1]]]
            tieline_points = np.array(group_phases_refs.get_group(key)[components])
            tp.plot(tieline_points, ax, color = color, marker = marker, ls="none", label = "", **kwargs)
    
    if legend_status:
        f_style = lambda m: plt.plot([],[],marker=m, color = "k", ls="none")[0]
        f_hue = lambda c: plt.plot([],[],marker="o", color = c, ls="none")[0]
        handles_style = [f_style(markers[i]) for i in range(len(style_unique))]
        handles_hue = [f_hue(colors[i]) for i in range(len(hue_unique))]
    
        first_legend = ax.legend(handles_style, style_unique, title = style, title_fontsize = 14, fontsize = 12, frameon=False, bbox_to_anchor=(0.15, 1)) #
        
        first_legend.set_draggable(True)
        plt.gca().add_artist(first_legend)    
        
        second_legend = ax.legend(handles_hue, hue_unique, title = hue, title_fontsize = 14, fontsize = 12, frameon=False, bbox_to_anchor=(0.65, 1)) #
        second_legend.set_draggable(True)
    if title_status:
        plt.suptitle("{}".format(fig_name), fontsize = 16)
    if savefig:
        fig.savefig(fig_path + "{}.png".format(fig_name))
#    if legend_status:
#        handles = []
#        f_style = lambda m: plt.plot([],[],marker=m, color = "k", ls="none")[0]
#        f_hue = lambda c: plt.plot([],[],marker="o", color = c, ls="none")[0]
#        handles = plt.plot([],[], ls="none")
#        handles += [f_style(markers[i]) for i in range(len(style_unique))]
#        handles += plt.plot([],[], ls="none")
#        handles += [f_hue(colors[i]) for i in range(len(hue_unique))]
#        labels = np.concatenate([np.array([style]), style_unique, np.array([hue]), hue_unique])
#    
#        leg = ax.legend(handles, labels, loc="best", framealpha=1, frameon=True)
#        leg.set_draggable(True)
   
#    tp.plot(tieline_points, ax, color = "k", label = key, **kwargs)
    

