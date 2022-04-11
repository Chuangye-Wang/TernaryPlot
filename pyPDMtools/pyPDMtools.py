# -*- coding: utf-8 -*-
"""
Created on Thu Dec 16 10:37:08 2021

@author: ustcw
"""
import sys
import os
#import csv
import numpy as np
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QTableWidgetItem
from layout import Ui_MainWindow

from EDS_data import EDS_data
import EDS_mapping as edsmap
from imagetools import ImageBuilder, LineBuilder

from pathlib import Path
import matplotlib as mpl
mpl.use("Qt5Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import time

class pyPDMtools_GUI(QMainWindow):
    def __init__(self):
        # Initalize parent
        QMainWindow.__init__(self)
        
        # Initalize GUI layout
        self.setWindowIcon(QtGui.QIcon('myIcon.png'))
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.eds_data = None
        self.comps = None
        self.technique = "WDS"
        self.read_counts = False
        
        self.ib = None
        self.N = 0 # N is the row_number
        
#        # pre-selection before import files
#        self.ui.elements.clicked.connect(lambda: self.elements)
#        self.ui.technique.clicked.connect(lambda: self.technique)
#        self.ui.read_counts.clicked.connect(lambda: self.read_counts)
#        self.ui.image_plot.clicked.connect(lambda: self.plotting('image'))
#        self.set_combo_Elements(self.comps)
#        self.set_combo_DataElements(self.comps)
        self.set_default_elements()
        self.ui.image_plot.clicked.connect(lambda: self.image_plots())
        self.ui.line_plot.clicked.connect(lambda: self.line_plots())
        self.ui.datashow.clicked.connect(lambda: self.show_data())
        
        self.ui.actionImport_folder.triggered.connect(lambda: self.import_message())
        self.ui.actionImport_folder.triggered.connect(lambda: self.import_data("folder"))
        self.ui.actionImport_file.triggered.connect(lambda: self.import_message())
        self.ui.actionImport_file.triggered.connect(lambda: self.import_data("file"))
        self.ui.actionExport.triggered.connect(lambda: self.export_data())
        self.ui.actionAbout.triggered.connect(self.about)
        
    
    def set_default_elements(self):
        self.ui.combo_E1.setCurrentIndex(5)
        self.ui.combo_E2.setCurrentIndex(6)
        self.ui.combo_E3.setCurrentIndex(7)
        
        self.ui.combo_Colormap.setCurrentIndex(1)
        
        self.ui.tableWidget_pick.setRowCount(100)
        self.ui.tableWidget_pick.setShowGrid(True)


    def set_combo_Elements(self, elems):
        """ To set the elements for mapping plot.
        """
        _translate = QtCore.QCoreApplication.translate
        self.ui.combo_Element.setItemText(0, _translate("MainWindow", "Element"))
        self.ui.combo_Element.setItemText(1, _translate("MainWindow", elems[0]))
        self.ui.combo_Element.setItemText(2, _translate("MainWindow", elems[1]))
        self.ui.combo_Element.setItemText(3, _translate("MainWindow", elems[2]))
        self.ui.combo_Element.setCurrentIndex(1)
    
    
    def set_combo_DataElements(self, elems):
        """ To set the elements for showing data
        """
        _translate = QtCore.QCoreApplication.translate
        self.ui.combo_DataElement.setItemText(0, _translate("MainWindow", "Element"))
        self.ui.combo_DataElement.setItemText(1, _translate("MainWindow", elems[0]))
        self.ui.combo_DataElement.setItemText(2, _translate("MainWindow", elems[1]))
        self.ui.combo_DataElement.setItemText(3, _translate("MainWindow", elems[2]))
        self.ui.combo_DataElement.setCurrentIndex(1)
    
    
    def import_data(self, type = "folder"):
        """ To import all comps files for each element from the folder.
        """
        # check if input elements is valid.
        self.pre_import_setting()
        
        if (not self.is_valid_elements()):
            return
        
        if type == "folder":
            path = QFileDialog.getExistingDirectory(None, "Please select a folder") 
            folder_path = str(path) + "/"
                
            self.eds_data = EDS_data(folder_path, self.comps, self.technique, read_counts = self.read_counts)
            self.statusBar().showMessage('Import folder successfully!', 2000)
        
        elif type == "file":
            # file dialog pop up, user can choose a csv or a txt file
            path, ext = QFileDialog.getOpenFileName(None, "Please select a file", "", "All Files (*);; CSV files (*.csv);; TXT files (*.txt)") 
            folder_path = str(Path(path).parent) + "\\"
            # return if there are no path or the file format is not correct
            if not (path.endswith('.csv') or path.endswith('.txt')):
                return
        
        self.after_import_setting()
    
    
    def export_data(self):
#        options = QFileDialog.Options()
#        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, 
                                                  "Save a data file", 
                                                  os.getcwd(), 
                                                  "csv Files (*.csv);; txt Files (*.txt);; All Files (*)", 
#                                                  options = options
                                                  )
        if fileName:
#            print(fileName)
            data_save = self.transfer_data()
            data_save.to_csv(fileName, index = False)
            self.statusBar().showMessage(f'Save data to {fileName} successfully!', 2000)
                
    def transfer_data(self):
        df = pd.DataFrame()
        row_num = self.ui.tableWidget_pick.rowCount()
        col_num = self.ui.tableWidget_pick.columnCount()
#        print(self.ui.tableWidget_pick.selectedItems())
        for col in range(col_num):
            col_name = str(self.ui.tableWidget_pick.horizontalHeaderItem(col).text())
            col_list = []
            for row in range(row_num):
                data1 = self.ui.tableWidget_pick.item(row, col)
                if data1 is not None:
                    col_list.append(float(data1.text()))
                else:
                    col_list.append(np.nan)
            df[col_name] = col_list
            
        return df
    
        
    def pre_import_setting(self):
        e1 = str(self.ui.combo_E1.currentText())
        e2 = str(self.ui.combo_E2.currentText())
        e3 = str(self.ui.combo_E3.currentText())
        self.comps = [e1, e2, e3]
        self.set_combo_Elements(self.comps)
        self.set_combo_DataElements(self.comps)
    
    
    def after_import_setting(self):
        e1 = str(self.ui.combo_E1.currentText())
        e2 = str(self.ui.combo_E2.currentText())
        e3 = str(self.ui.combo_E3.currentText())
        self.ui.tableWidget_pick.setHorizontalHeaderItem(0, QTableWidgetItem(e1))
        self.ui.tableWidget_pick.setHorizontalHeaderItem(1, QTableWidgetItem(e2))
        self.ui.tableWidget_pick.setHorizontalHeaderItem(2, QTableWidgetItem(e3))
    
    
    def show_data(self):
        """ To present data in the tabular area / table.
        """
        if (self.eds_data == None):
            text = "Please import data first, then show the comp data."
            self.ui.datashow.clicked.connect(lambda: self.message_connect(text))
            return
        
        e1 = str(self.ui.combo_E1.currentText())
        e2 = str(self.ui.combo_E2.currentText())
        e3 = str(self.ui.combo_E3.currentText())
        
        if (not self.is_valid_elements()):
            text = f"Wrong Elements selection: {e1}, {e2}, {e3}."
            self.ui.datashow.clicked.connect(lambda: self.message_connect(text))
            return
        
        current_element = str(self.ui.combo_DataElement.currentText())
        if current_element not in self.comps:
            text = f"Selected element {current_element} is not in [{e1}, {e2}, {e3}]."
            self.ui.datashow.clicked.connect(lambda: self.message_connect(text))
            return
        
        data_show = self.eds_data.data[current_element]
        num_row, num_col = data_show.shape
        self.ui.tableWidget.setColumnCount(num_col)
        self.ui.tableWidget.setRowCount(num_row)
        
        for i in range(num_row):
            for j in range(num_col):
                self.ui.tableWidget.setItem(i, j, QTableWidgetItem(str(data_show[i, j])))
        
        self.ui.tableWidget.resizeColumnsToContents()
    
    
    def message_connect(self, message_text):
        """ To show error message and remind user what to do to fix the error.
        """
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText(message_text)
#        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)      
        msg.exec()
    
    
    def import_message(self):
        """ To show error message in importing folder/files and remind user what to do to fix the error.
        """
        if (self.is_valid_elements()): return
        
        msg = QMessageBox()
        msg.setWindowTitle("Error")
        msg.setText("Please select valid elements first.")
#        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)      
        msg.exec()
        
    
    def closeEvent(self, event):
        """Generate 'question' dialog on clicking 'X' button in title bar.

        Reimplement the closeEvent() event handler to include a 'Question'
        dialog with options on how to proceed - Save, Close, Cancel buttons
        """        
        reply = QMessageBox.question(
            self, "Message",
            "Are you sure you want to quit?",
            QMessageBox.Save | QMessageBox.Close | QMessageBox.Cancel,
            QMessageBox.Save)

        if reply == QMessageBox.Close:
            event.accept()
        else:
            event.ignore()
    
    
    def is_valid_elements(self) -> bool:
        """ To check if the three elements are valid.
        """
        e1 = str(self.ui.combo_E1.currentText())
        e2 = str(self.ui.combo_E2.currentText())
        e3 = str(self.ui.combo_E3.currentText())
        
        if (e1 == "E1" or e2 == "E2" or e3 == "E3"): return False
        
        set1 = set({e1, e2, e3})
        if (len(set1) < 3): return False
        
        return True
        
    
    def line_plots(self):
        """
        still in test mode
        """
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(111)
        ax.set_xlim([-1,6])
        ax.set_ylim([-1,6])
        ax.plot([0,1,2,3,4,5],[0,1,2,3,4,5],'o--')
        canvas = FigureCanvas(fig)
#        toolbar = NavigationToolbar(canvas, self)
        graphicscene = QtWidgets.QGraphicsScene(0, 0, 650, 610)
#        graphicscene.addWidg
        graphicscene.addWidget(canvas)
        self.ui.line.setScene(graphicscene)
#        self.ui.line.fitInView(graphicscene, True)
        self.ui.line.show()

        
    def image_plots(self):
        current_element = str(self.ui.combo_Element.currentText())
        current_cmap = str(self.ui.combo_Colormap.currentText())
        figsize = 8
        fig, ax = edsmap.colormap2d(self.eds_data.data[current_element], figsize = figsize, cmap = current_cmap, close = False)
        self.show_picked_data()
        # update N
        if (self.ib is not None):
            count = 0
            for ibs in self.ib.linebuilder:
                count += max([len(ib.coords) for ib in ibs])
            self.N += count
        print("N = ", self.N)
        self.set_image_interactive(fig, ax)
#        canvas = FigureCanvas(fig)
#        
##        toolbar = NavigationToolbar(canvas, self)
#        layout = QtWidgets.QVBoxLayout()
##        layout.addWidget(toolbar)
#        layout.addWidget(canvas)
##        self.ui.image_toolbar.setLayout(layout)
#        
##        graphicscene = QtWidgets.QGraphicsScene(0, 20, figsize / 2*100, figsize / 2*100)
##        graphicscene.addWidget(canvas)
##        self.ui.image.setScene(graphicscene)
#        self.ui.image.setLayout(layout)
##        self.setCentralWidget(widget)
##        self.ui.image.setInteractive(True)
    
    
    def show_picked_data(self):
        """ To present the picked data from interactive comp-dis profiles.
        """
        
        
    def set_image_interactive(self, fig, ax):
        self.ib = ImageBuilder(fig, ax, self.eds_data.data) #, self.N, self.ui.tableWidget_pick
        
    
    def show_figure(self, fig):
        # create a dummy figure and use its
        # manager to display "fig"
    
        dummy = plt.figure()
        new_manager = dummy.canvas.manager
        new_manager.canvas.figure = fig
        fig.set_canvas(new_manager.canvas)
    
    
    def about(self):
        QMessageBox.about(
            self,
            "About Phase Diagram Mapping",
            "<p>Map the phase diagram of ternary system based on the composition measurements form EDS/WDS mapping techniques, this app is built with:</p>"
            "<p>- PyQt</p>"
            "<p>- Qt Designer</p>"
            "<p>- Python</p>",
        )
        
        
class Figure_Canvas(FigureCanvas):
    def __init__(self, fig = None, parent=None, width=6, height=4.8, dpi=100):
        # create Figure under matplotlib.pyplot
        # deactivate the popping of another figure panel
        self.setParent(parent) 
        plt.ioff()
#        plt.rc('text', usetex=True)
        plt.rc('font', family='serif', size = 20)
        plt.rc('xtick', labelsize = 15)
        plt.rc('ytick', labelsize = 15)
        if fig == None: 
            fig = plt.figure(figsize=(width, height), dpi=dpi)
            self.axes = fig.add_subplot(111) # using add_subplot method
            fig.tight_layout()
            fig.subplots_adjust(left=0.14, bottom=0.13, right=0.9, top=0.9)
        
        # initalizing parent
#        fig.tight_layout()
        FigureCanvas.__init__(self, fig)
        
    def show_figure(fig):
        # create a dummy figure and use its
        # manager to display "fig"  
        dummy = plt.figure()
        new_manager = dummy.canvas.manager
        new_manager.canvas.figure = fig
        fig.set_canvas(new_manager.canvas)
            

if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()
   
    app.setQuitOnLastWindowClosed(True)
#    app.setQuitLockEnabled(True)
    MainWindow = pyPDMtools_GUI()
    MainWindow.show()
#    MainWindow.centralWidget().show()
    app.exec_()
    app.quit()
#    sys.exit(app.exec_())