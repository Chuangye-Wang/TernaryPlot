# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 16:36:12 2021

@author: ustcw
"""
import pandas as pd
import numpy as np


class EDS_data():
     """ This is used for EDS data mapping process """
     def __init__(self, path, comps, technique = "EDS", midfix = "Comps", read_counts = False):
          """ Build a constructor with the input parameter
   
          file_name: the name of file including the directory path;
          comps: the components of a ternary system;
             
          """
          self.comps = comps
          self.midfix = midfix
          self.technique = technique.upper()
          data = self.read_comps_data(path)
          self.data = data
          self.counts = None
          if read_counts: self.counts = self.read_counts_data(path)
          
          
     def read_comps_data(self, path):
          """ Read data from .csv file
                  
          Return: a dict of 3 values of array with cols and rows.
          """
          if (len(self.comps) < 2 or len(self.comps) > 3): raise ValueError("Length of comps list should be equal to 2 or 3.")
          comps_order = self.comps
          file_var = ""
          for i in range(len(self.comps) - 1):
               file_var += self.comps[i] + "-"
          file_var += self.comps[len(self.comps) - 1] + "_"
          filePath = path
          filename = [file_var + self.midfix + "_" + elem + ".csv" for elem in comps_order]
          data = {}
               
          for i in range(len(self.comps)):
               # Because the sum of composition is 10000, so each data is divided by 100 to get atomic percent value; 
               data[self.comps[i]] = np.array(pd.read_csv(filePath + filename[i]))
                  
          return data       
     
     
     def read_counts_data(self, path):
          """ To calculate the counts at every measure dot.
          """
          if (len(self.comps) < 2 or len(self.comps) > 3): raise ValueError("Length of comps list should be equal to 2 or 3.")
          comps_order = self.comps
          file_var = ""
          for i in range(len(self.comps) - 1):
               file_var += self.comps[i] + "-"
          file_var += self.comps[len(self.comps) - 1] + "_"
          counts = np.zeros(self.data[self.comps[0]].shape)
          
          if self.technique == "EDS":
              filename = [file_var + "Counts_" + elem + ".csv" for elem in comps_order]
              data_counts = {}
              
              try:
                   for i in range(len(self.comps)):
                        data_counts[self.comps[i]] = pd.read_csv(path + filename[i])
                        counts += np.array(data_counts[self.comps[i]]) * np.array(self.data[self.comps[i]]) / 100
              except: pass
          elif self.technique == "WDS":
              try:
                  counts = np.array(pd.read_csv(path + file_var + "Counts.csv"))
              except: pass
              
          return counts

    
     def select_data_area(self, x_min = 0, y_min = 0, x_max = 1, y_max = 1, data_type = 'comps'):
          """ Select the data to be used
          x_min: start point in x axis (fraction of the x range)
          y_min: start point in y axis (fraction of the y range)
          x_max: end point in x axis (fraction of the x range)
          y_max: end point in y axis (fraction of the y range)
        
          Return: cut comps, or counts;
          """
          if not isinstance(data_type, str): raise TypeError("data_type is not a string.")
          if (data_type != 'comps' and data_type != 'counts'): raise ValueError("Input of data_type is wrong. Please select from comps, counts.")
          x_min = self.data[self.comps[0]].shape[1] * x_min
          y_min = self.data[self.comps[0]].shape[0] * y_min
          x_max = self.data[self.comps[0]].shape[1] * x_max
          y_max = self.data[self.comps[0]].shape[0] * y_max
          data_array1 = {}
          
          if data_type == 'comps':
               for i in range(len(self.comps)):
                    # it is divided by 100 because if should be calculated by 
                    data_array1[self.comps[i]] = self.data[self.comps[i]][y_min: y_max, x_min: x_max]
                 
               return data_array1
          elif data_type == 'counts':
               return self.counts[y_min: y_max, x_min: x_max]
          
     def lowCountsScreen(self, index = -1, threshold = 10, replace = np.nan):
          """ Screen the data with low counts. Update the self.data.
          threshold
          
          return no
          """
          data_array = {}
          if (index >= 0 and index < len(self.comps)): return np.where(self.counts >= threshold, self.data[self.comps[index]], replace)
          else:
               for i in range(len(self.comps)):
                   data_array[self.comps[i]] = np.where(self.counts >= threshold, self.data[self.comps[i]], replace) 
                   
               return data_array
               
    

   
        
        