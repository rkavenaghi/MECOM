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
            self.grNode.resize(300, 350)

            inputs = [0.25, 0.38, 0.51, 0.65, 0.77]
            outputs = [0.87, {'pos':.94, 'type': 'complex'}] # Saida de h(t)
        
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
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)
        # Massa 
        f1 = QFrame()
        l1 = SVGLabel().load('m - [kg]')
        l1.setMaximumHeight(20)
        e1 = QLineEdit()
        layout1 = QHBoxLayout()
        f1.setLayout(layout1)
        layout1.addWidget(l1)
        layout1.addWidget(e1)
        # Rigidez 
        f2 = QFrame()
        l2 = SVGLabel().load('k - [N/m]')
        l2.setMaximumHeight(20)
        e2 = QLineEdit()
        layout2 = QHBoxLayout()
        f2.setLayout(layout2)
        layout2.addWidget(l2)
        layout2.addWidget(e2)
        # Amortecimento
        f3 = QFrame()
        l3 = SVGLabel().load('c - [N.s/m]')
        l3.setMaximumHeight(20)
        e3 = QLineEdit()
        layout3 = QHBoxLayout()
        f3.setLayout(layout3)
        layout3.addWidget(l3)
        layout3.addWidget(e3)
        f4 = QFrame()
        l4 = QLabel('IN4 - Vetor t')
        l5 = QLabel('IN5 - Vetor omega')

        layout4 = QHBoxLayout()
        
        layout4.addWidget(l4)
        
        f4.setLayout(layout4)
        
        layout5 = QHBoxLayout()
        layout5.addWidget(l5)
        f5 = QFrame()
        f5.setLayout(layout5)

        self.entrys = [e1, e2, e3]
        for entry in self.entrys:
            entry.setText('')
            entry.textEdited.connect(self.node.updateNode)


        self.layout.addWidget(QLabel('Sistema Mecânico de 1 GDL'))
        for frame in [f1, f2, f3, f4, f5]:
            self.layout.addWidget(frame)

        out1 = SVGLabel()
        out1.load('h(t)')
        out1.setFixedSize(30, 20)
        self.layout.addWidget(out1)

        out2 = SVGLabel()
        out2.load('H(f)')
        out2.setFixedSize(30, 20)
        self.layout.addWidget(out2)

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
