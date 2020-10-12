
import numpy as np
import os

from PyQt5.QtWidgets import (QApplication,QLabel,QMainWindow,QComboBox,QPushButton,QWidget,QListWidget,QListWidgetItem,
                             QHBoxLayout,QVBoxLayout,QGridLayout, QMainWindow,QMenuBar,QTextEdit,QListView,QFrame,
                             QMdiArea,QGraphicsView,QGraphicsScene,QGraphicsWidget,QMdiSubWindow,QTreeView,QTreeWidget,
                             QTreeWidgetItem,QDockWidget,QTabWidget,QGraphicsItem,QDialog)
from PyQt5.QtGui import QPainter,QPen,QBrush,QMouseEvent,QIcon

from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt,QEvent,pyqtSignal

from functools import partial
import importlib


from documentation_widget import *
import logging

class QDMTreeWidgetCustom(QTreeWidget):
    #parent = self.object_tree_documentation
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.current_item = None

    def mousePressEvent(self,event):
    # Redefine Mouse Events
        try:
            self.current_item.widget.close()
        except:
            pass
                

        self.current_item = self.itemAt(event.pos())
        
        if event.button() == Qt.RightButton:
            if type(self.current_item) == QTreeWidgetItem:

                self.current_item.widget = QWidget(self)
                layout = QVBoxLayout(self.current_item.widget)
                

                b1 = QPushButton('Propriedades')
                b2 = QPushButton('Deletar Nó')
                b3 = QPushButton('Duplicar')
                b4 = QPushButton('Esconder')
                b5 = QPushButton('Fechar')

                #self.current_item.widget.setStyleSheet('background: #afaa71')
                for botao in [b1,b2,b3,b4,b5]:
                    layout.addWidget(botao)
                    botao.clicked.connect(self.qwidgetItemMenu)
                self.current_item.widget.move(event.pos().x(),event.pos().y())
                self.current_item.widget.show()

        if event.button() == Qt.LeftButton:
            if isinstance(self.current_item, QTreeWidgetItem):
                if hasattr(self.current_item, 'node'):
                    node = self.current_item.node
                    node.setSelected(True)

        super().mousePressEvent(event) # Utilizado para manter as outras funcionalidades do método

    def qwidgetItemMenu(self):
        botao_clicado = self.sender()
        if (botao_clicado.text() == 'Fechar'):
            try:
                self.current_item.widget.close()
            except:
                pass
        elif botao_clicado.text() == 'Deletar Nó':

            item = self.current_item.node
            print(self.current_item)
            parent = self.current_item.parent() #Parent nesse caso é um node

            root = self.invisibleRootItem()
            root.removeChild(self.current_item)

            item.parent.object_names.remove(self.current_item.text(0))
            item.removeNode()

            self.current_item.widget.close()
                  

        elif botao_clicado.text() == 'Propriedades':
            # Abrir um novo menu com as propriedades detalhadas do objeto.
            try:
                self.current_item.widget.close()
            except:
                pass
  
            self.current_item.widget = QDMPropertiesWidget(self)
            
            
        else:
            print('Nao Implementado')

class QDMPropertiesWidget(QDialog):
    def __init__(self,parent = None):
        super().__init__(parent)
        
        self.parent = parent
        self.resize(600,400)
        self.initUI()
    def initUI(self):
        # Printar os inputs. Carregar o Node desse item
        node = self.parent.current_item.node
        
        layout = QVBoxLayout(self)

        self.setWindowTitle('Propriedades do Nó')
        layout.addWidget(QLabel(f'Nome: {self.parent.current_item.text(0)}'))



        

        for counter,inputs in enumerate(node.inputs):
            frame = QFrame()
            flayout = QHBoxLayout()
            frame.setLayout(flayout)
            
            lbel = QLabel(f'INPUT {counter}:')
            flayout.addWidget(lbel)
            if inputs.hasEdge():
                flayout.addWidget(QLabel(f'Edge conectada à {inputs.edge.end_socket}'))

            layout.addWidget(frame)
        for counter,outputs in enumerate(node.outputs):

            frame = QFrame()
            flayout = QHBoxLayout()
            frame.setLayout(flayout)
            lbel = QLabel(f'OUTPUT {counter}:')
            flayout.addWidget(lbel)
            if outputs.hasEdge():
                flayout.addWidget(QLabel(f'Edge conectada à {outputs.edge.end_socket}'))

            layout.addWidget(frame)



        #        children = []
        #for child in range(item.childCount()):
        #    children.append(item.child(child))
        #for child in children:
        #    item.removeChild(child)
        self.show()

    def keyPressEvent(self,event):


        super().keyPressEvent(event)