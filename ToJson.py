# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 22:39:49 2021

@author: ustcw
"""

import json
import jsbeautifier
import pandas as pd
import numpy as np
import os.path
#import math
#import os

def createFileName(filenames):
    """
    filenames: a list or array
    
    returns: a string contains filenames connected by dashed line -
    """
    name = ""
    for filename1 in filenames[:-1]:
        name += filename1.upper() + "-"
    name += filenames[-1]
    
    return name
def ternaryToJson(filename, jsonfile = "", outputfilepath = "", sheetname = "Tie lines", output = "ZPF"):
    """
    To convert a spreadsheet file with phase information of ternary system to json file 
    
    filename: string, the location path of data file in csv or excel format.
    jsonfile: string, the final desired and saved json file 
    sheetname: string, the sheetname for differetn types of data. It includes "Unary phase", "Tie lines" 
    
    return: none
    """
    file_extension = os.path.splitext(filename)[1]
    if file_extension == '.csv':
        data = pd.read_csv(filename)
    elif file_extension == '.xls' or file_extension == '.xlsx':
        if sheetname == "default":
            sheetname = os.path.splitext(filename)[0]
        data = pd.read_excel(filename, sheet_name = sheetname)
    if "Components" in data.columns:
        components = list(data["Components"].dropna())
    else: raise NameError("Components are not in inputfile's columns names")
#    elements_number = len(components)

#    refs_content = ""
    comp1 = components[0]
    comp2 = components[1]
    
    options = jsbeautifier.default_options()
    options.indent_size = 4
    
    if sheetname == "Tie lines":
        if "Ref" in data.columns and (not data["Ref"].isnull().values.all()):
            Refs = data["Ref"].unique()
            for ref in Refs:
                df_ref = data[data["Ref"] == ref]
                Temps = list(df_ref["T/K"])
                if "Phase 3" in df_ref.columns:
                    phases = list(np.unique(np.concatenate([df_ref["Phase 1"].dropna().unique(), df_ref["Phase 2"].dropna().unique(), df_ref["Phase 3"].dropna().unique()])))
                else:
                    phases = list(np.unique(np.concatenate([df_ref["Phase 1"].dropna().unique(), df_ref["Phase 2"].dropna().unique()])))
                if jsonfile == "":
                    jsonfile_list = components + [output] + phases + [ref+".json"]
                    jsonfile_name = createFileName(jsonfile_list)
                    filepath = os.path.join(outputfilepath, jsonfile_name)
                    if not os.path.exists(filepath):  # create a json file
                        # os.makedirs(path1)
                        open(filepath, 'w')
                else:
                    filepath = jsonfile
                                
                phase1_comp1 = comp1 + "_" + "1"
                phase1_comp2 = comp2 + "_" + "1"
                phase2_comp1 = comp1 + "_" + "2"
                phase2_comp2 = comp2 + "_" + "2"
                phase3_comp1 = comp1 + "_" + "3"
                phase3_comp2 = comp2 + "_" + "3"
                phase_data = []
                for i in df_ref.index:
                    phase1 = [df_ref["Phase 1"][i], [comp1, comp2], [df_ref[phase1_comp1][i], df_ref[phase1_comp2][i]]]
                    phase2 = [df_ref["Phase 2"][i], [comp1, comp2], [df_ref[phase2_comp1][i], df_ref[phase2_comp2][i]]]
                    if not pd.isna(df_ref["Phase 3"][i]):
                        phase3 = [df_ref["Phase 3"][i], [comp1, comp2], [df_ref[phase3_comp1][i], df_ref[phase3_comp2][i]]]
                        phase_data.append([phase1, phase2, phase3])
                    else: phase_data.append([phase1, phase2])
                data_dict = {
                        "components": components,
                        "phases": phases,
                        "broadcast_conditions": False,
                        "conditions": {
                            "T":  Temps,
                            "P": [101325]
                        },
                        "output": output,
                        "values": phase_data,
                        "reference": ref,
                        "comment": ""
                }
#                json_object = json.dumps(data_dict, indent = 4)
                json_object = jsbeautifier.beautify(json.dumps(data_dict), options)
                # write jsonfile
                with open(filepath, 'w') as outfile:
                    outfile.write(json_object)


def binaryToJson(filename, jsonfile = "", outputfilepath = "", sheetname = "default", output = "ZPF"):
    """
    filename: string
    path: string
    
    return: none
    """
    file_extension = os.path.splitext(filename)[1]
    if file_extension == '.csv':
        data = pd.read_csv(filename)
    elif file_extension == '.xls' or file_extension == '.xlsx':
        if sheetname == "default":
            sheetname = os.path.splitext(filename)[0]
        data = pd.read_excel(filename, sheet_name = sheetname)
    if "Components" in data.columns:
        components = list(data["Components"].dropna())
    else: raise NameError("Components are not in inputfile's columns names")
    
    options = jsbeautifier.default_options()
    options.indent_size = 4
    
    if sheetname == "Tie lines":
        if "Ref" in data.columns and (not data["Ref"].isnull().values.all()):
            Refs = data["Ref"].unique()
            for ref in Refs:
                df_ref = data[data["Ref"] == ref]
                Temps = list(df_ref["T/K"])
                if "Phase 3" in df_ref.columns:
                    phases = list(np.unique(np.concatenate([df_ref["Phase 1"].dropna().unique(), df_ref["Phase 2"].dropna().unique(), df_ref["Phase 3"].dropna().unique()])))
                else:
                    phases = list(np.unique(np.concatenate([df_ref["Phase 1"].dropna().unique(), df_ref["Phase 2"].dropna().unique()])))
                if jsonfile == "":
                    jsonfile_list = components + [output] + phases + [ref+".json"]
                    jsonfile_name = createFileName(jsonfile_list)
                    filepath = os.path.join(outputfilepath, jsonfile_name)
                    if not os.path.exists(filepath):  # create a json file
                        # os.makedirs(path1)
                        open(filepath, 'w')
                else:
                    filepath = jsonfile
                comp1 = components[0]
                phase1_comp1 = comp1 + "_" + "1"
                phase2_comp1 = comp1 + "_" + "2"
        
                phase_data = []
                for i in df_ref.index:
                    phase1 = [df_ref["Phase 1"][i], [comp1], [df_ref[phase1_comp1][i]]]
                    phase2 = [df_ref["Phase 2"][i], [comp1], [df_ref[phase2_comp1][i]]]
                    phase_data.append([phase1, phase2])
                    data_dict = {
                            "components": components,
                            "phases": phases,
                            "broadcast_conditions": False,
                            "conditions": {
                                "T":  Temps,
                                "P": [101325]
                            },
                            "output": output,
                            "values": phase_data,
                            "reference": ref,
                            "comment": ""
                    }

                json_object = jsbeautifier.beautify(json.dumps(data_dict), options)
                with open(filepath, 'w') as outfile:
                    outfile.write(json_object)        
#    json_object = json.dumps(new_data, indent = 4)   #, separators = (',', ': ')
#    print(type(json_object))
#    with open('data.json', 'w') as outfile:
##        outfile.write(json.dumps(["BCC"]))
#        outfile.write(json_object)
#    with open('data.json', 'w') as outfile:
#        json.dump(new_data, outfile, indent = 4)
    

if __name__ == "__main__":
    pass