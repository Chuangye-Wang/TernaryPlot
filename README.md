# TernaryPlot
(1). Plotting 3d data in 2d ternary diagram. The 3 components are denoted by A, B, C.
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/examples_figure1.png" width="600" alt="Phase Diagram">
</p>

(2). Magnify the selected red triangle in (1) to an equilateral triangle.
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/examples_figure1_zoom-in.png" width="600" alt="Phase Diagram">
</p>

(3). For the theories behind mapping a arbitrary triangle to an equilateral triangle, one could refer to this discussion in stackexchange https://math.stackexchange.com/questions/541926/converting-triangles-to-isosceles-equilateral-or-right

(4). Quickly plot phase boundaries data with tielines_plot in plots.py.

There are two modes:

mode = 1: Plot the literature in the different colors and markers (does not show the phase information)

mode = 2: Plot the phases in different markers and the literature in different colors
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/tie-line-figure_mode1.png" width="600" alt="Phase Diagram">
</p>
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/tie-line-figure_mode2.png" width="600" alt="Phase Diagram">
</p>

# EDS data and imagetools
(1). Heatmapping with a random array of size 100x100.
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/EDS-figure.png" width="600" alt="Phase Diagram">
</p>

(2). Heatmapping of Nb element in Fe-Nb-Ni triple area. Select two points in the heatmap and plot the composition versus distance profiles.
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/Nb_heatmap.png" width="600" alt="Phase Diagram">
</p>
<p float="left">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/Fe_comp_dis.png" width="260">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/Nb_comp_dis.png" width="260">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/Ni_comp_dis.png" width="260">
</p>

# Tojson
Transfer the data in the spreadsheet to the json file with required format for future thermodynamic assessment

# Gui usage
Integrate the load data, view data, plotting heatmap, extracting datapoints, save data into a gui.
<p align="center">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/interface_view.JPG" width="600" alt="Phase Diagram">
  <img src="https://github.com/Chuangye-Wang/TernaryPlot/blob/main/example_figures/interface_workflow.JPG" width="600" alt="Phase Diagram">
</p>
