# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 10:08:31 2021

@author: ustcw
"""

import pyTernary.EDS_mapping as eds
import numpy as np

size = 100
data = np.ones((size, size))
for i in range(10):
     data[:, 10*i:10*(i+1)] = np.random.randint(10*i, 10*(i+1) - 1, size = (100, 10))
eds.colormap2d(data, cmap = "gist_rainbow")