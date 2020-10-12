import numpy as np

from core.node import *
from core.node_socket import *


class Node_complex(Node):
    """
    Este nó serve para separar o número de interesse.

    IN: x
    ---- x: array com dimensão N 
    OUT: y
    ---- y: array com dimensão N
        
    """
    
    def __init__(self, scene, title="Bloco complexo", parent=None, method=None):
        super().__init__(Node=self)
        
        self.MODULO = 'Complexo'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent 
        self.title = title
        
        self.content = QDMNodeComplex(self) #mando o node tambem
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(200, 200)

        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        inputs = [{'pos':0.25, 'type': 'complex'}]
        
        outputs = [{'pos': 0.42, 'type': 'float'},
                   {'pos': 0.58, 'type': 'float'},
                   {'pos': 0.75, 'type': 'float'},
                   {'pos': 0.90, 'type': 'float'}]

        self.inputs = []
        self.outputs = []

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()


class QDMNodeComplex(QWidget):
    def __init__(self,node,parent = None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.layout.addWidget(QLabel('IN1: x'))
        self.layout.addWidget(QLabel('OUT1: Re(x)'))
        self.layout.addWidget(QLabel('OUT2: Im(x)'))
        self.layout.addWidget(QLabel('OUT3: Abs(x)'))
        self.layout.addWidget(QLabel('OUT4: Fase(x)'))

    def refresh(self):
        if self.node.inputs[0].hasEdge():
            if not isinstance(self.node.inputs[0].edge.data,type(None)):
                try:
                    x = self.node.inputs[0].edge.data
                    self.node.sendSignal([x.real, x.imag, abs(x), np.arctan2(x.imag, x.real)],
                                         self.node.outputs,
                                         [self, self, self, self],
                                         ['float', 'float', 'float', 'float'])

                except:
                    self.node.invalidSignal()



