import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import tikzplotlib

from functools import partial

import numpy as np

plt.style.use('ggplot')
from PyQt5.QtWidgets import (QApplication,QLabel,QMainWindow,QComboBox,QPushButton,QWidget,QListWidget,QListWidgetItem,
                             QHBoxLayout,QVBoxLayout,QGridLayout, QMainWindow,QMenuBar,QTextEdit,QListView,QFrame,
                             QMdiArea,QMdiSubWindow,QTreeView,QTreeWidget,QTreeWidgetItem,QDockWidget,QToolBox)
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt


def gui_configuration(subwindow,parent):
    
    frame = QFrame()
    layout = QVBoxLayout()
    pushButton1 = QPushButton('Sistemas Lineares')
    

    toolbox = QToolBox()
    label = QLabel('Sistemas de primeira ordem')
    label2= QLabel('Sistemas de segunda ordem')
    toolbox.addItem(label,'Sistemas 1 ordem')
    toolbox.addItem(label2,'Sistemas 2 ordem')
    

    layout.addWidget(pushButton1)
    
    layout.addWidget(toolbox)
    frame.setLayout(layout)
    subwindow.setWidget(frame)
    return subwindow

if __name__=='__main__':
    tau = 0.1
    K = 1
    s = np.linspace(0,100,100)
    H = lambda s:K/(tau*s +1)
    
    fig,ax = plt.subplots(nrows=1)

    ax.plot(s,H(s))
    plt.show(fig)
    
    #resposta temporal para sistema de primeira ordem 
    