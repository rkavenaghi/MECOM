import numpy as np
import os

from PyQt5.QtWidgets import (QApplication,QLabel,QMainWindow,QComboBox,QPushButton,QWidget,QListWidget,QListWidgetItem,
                             QHBoxLayout,QVBoxLayout,QGridLayout, QMainWindow,QMenuBar,QTextEdit,QListView,QFrame,
                             QMdiArea,QGraphicsView,QGraphicsScene,QGraphicsWidget,QMdiSubWindow,QTreeView,QTreeWidget,
                             QTreeWidgetItem,QDockWidget,QTabWidget,QGraphicsItem,QDialog)
from PyQt5.QtGui import QPainter,QPen,QBrush,QMouseEvent

from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt,QEvent,pyqtSignal

from functools import partial
import importlib

class Documentation(QMainWindow):
    def __init__(self,parent = None ):
        print('Documentacao')
        super().__init__(parent)
        self.parent = parent
        self.setWindowTitle('Ajuda')
        self.top = 100
        self.left = 300
        self.width = 680
        self.height = 500
        self.setGeometry(self.top, self.left, self.width, self.height)
        
        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)
        self.main_widget.setFocus()
        self.main_layout = QGridLayout()

        l1 = QTextEdit('Carregar a documentacao aqui' )
        l1.setReadOnly(True)
        
        self.main_layout.addWidget(l1,0,0)

        self.main_widget.setLayout(self.main_layout)
        
        self.show()