import numpy as np

from core.node import Node, QDMGraphicsNode
from utils.MECWidgets import SVGLabel
from core.node_socket import *
from toolboxes.vibrations.vibrations import Sdof

class Node_vibration(Node):
    def __init__(self,scene,title="Módulo de Vibrações Mecânicas", outputs=[], parent=None, method=None):
        super().__init__(Node=self)
        self.method = method
        self.MODULO = 'Vibrações'
        self.MODULO_INITIALIZED = False #Parametro utilizado para nomear nas arvores de objetos
        self.parent = parent
        self.scene = scene
        
        self.title = title

        if self.method == 'SDOF':
            self.content = QDMNodeSDOF(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(300, 300)

            inputs = [0.22, 0.38, 0.56, 0.71, 0.86]
            outputs = [0.71, {'pos': .86, 'type': 'complex'}]
        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

class QDMNodeSDOF(QWidget):
    def __init__(self,node, parent=None):
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        e1 = QLineEdit()
        e2 = QLineEdit()
        e3 = QLineEdit()

        self.layout.addWidget(SVGLabel().load('m - [kg]'), 0, 0)
        self.layout.addWidget(e1, 0, 1)

        self.layout.addWidget(SVGLabel().load('k - [N/m]'), 1, 0)
        self.layout.addWidget(e2, 1, 1)

        self.layout.addWidget(SVGLabel().load('c - [N.s/m]'), 2, 0)
        self.layout.addWidget(e3, 2, 1)



        self.entrys = [e1, e2, e3]
        for entry in self.entrys:
            entry.setText('')
            entry.textEdited.connect(self.node.updateNode)


        out1 = SVGLabel()
        out1.load('h(t)')
        out1.setFixedSize(30, 20)
        self.layout.addWidget(out1, 3, 0)

        out2 = SVGLabel()
        out2.load('H(f)')
        out2.setFixedSize(30, 20)
        self.layout.addWidget(out2, 4, 0)

    def haveEntrys(self):    
        e1, e2, e3 = self.entrys
        if (e1.text() =='' or e2.text()=='' or e3.text()==''):
            return False
        else:
            return True

    def refresh(self):
        entrySocket = [{'socket': self.node.inputs[0], 'entry': self.entrys[0]},
                       {'socket': self.node.inputs[1], 'entry': self.entrys[1]},
                       {'socket': self.node.inputs[2], 'entry': self.entrys[2]}]
        data = self.node.checkConnectedEdgeData(entrySocket)
        if self.haveEntrys():
            self.entrys_parameters = {'m': float(data[0]), 'k': float(data[1]), 'c': float(data[2])}
            system_sdof = Sdof() 
            system_sdof.parameters(self.entrys_parameters)
            if self.node.inputs[3].hasEdge():
                if not isinstance(self.node.inputs[3].edge.data, type(None)):
                    if (self.node.outputs[0].hasEdge()):
                        for edge in self.node.outputs[0].edges:
                            system_sdof.irf()
                            t = self.node.inputs[3].edge.data
                            h = system_sdof.h
                            edge.signal(h(t), self, data_type='float')

            if self.node.inputs[4].hasEdge():
                if not isinstance(self.node.inputs[4].edge.data, type(None)):
                     if (self.node.outputs[1].hasEdge()):
                        for edge in self.node.outputs[1].edges:
                            system_sdof.frf()
                            f = self.node.inputs[4].edge.data
                            H = system_sdof.receptance
                            edge.signal(H(2*np.pi*f), self, data_type='complex')
