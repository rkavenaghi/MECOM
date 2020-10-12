
import numpy as np

from core.node import *
from core.node_socket import *



import logging
import matplotlib.pyplot as plt
from utils.MECWidgets import SVGLabel


class Node_signals(Node):
    def __init__(self, scene, title="Sinais", parent=None,method = None,data_type='float'):
        super().__init__(self)
        self.data_type=data_type
        self.method = method
        self.scene = scene
        self.parent = parent
        self.MODULO_INITIALIZED = False

        self.title = method
        self.MODULO = method
        prosseguir = False
        if method == 'Seno':
            logging.info('Método SENO')
            self.content = QDMNodeSignalSeno(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(220, 250)
            inputs = [0.25, 0.45, 0.65, 0.81]
            outputs = [0.93]
            prosseguir = True
        if method == 'Impulso':
            logging.info('Impulso')
            self.content = QDMNodeSignalImpulse(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(200,200)
            inputs = [0.24, 0.4]
            outputs = [0.92]
            prosseguir = True

        else:
            logging.info('Não implementado ainda')

        if prosseguir:
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            self.inputs = []
            self.outputs=[]
            self.configInputsOutputs(inputs,outputs)
            self.configureObjectTree()

class QDMNodeSignalSeno(QWidget):
    def __init__(self, node, parent = None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        hframe1 = QFrame()
        hlayout1 = QHBoxLayout()
        hframe1.setLayout(hlayout1)

        hlayout1.addWidget(QLabel('IN1 : Amplitude'))
        e1 = QLineEdit()
        hlayout1.addWidget(e1)

        hframe2 = QFrame()
        hlayout2 = QHBoxLayout()
        hframe2.setLayout(hlayout2)
        hlayout2.addWidget(QLabel('IN2 : Frequência'))
        e2 = QLineEdit()
        hlayout2.addWidget(e2)



        hframe3 = QFrame()
        hlayout3 = QHBoxLayout()
        hframe3.setLayout(hlayout3)

        hlayout3.addWidget(SVGLabel().load('\phi', size=(25, 25)))
        e3 = QLineEdit()
        hlayout3.addWidget(e3)

        frames = [hframe1, hframe2, hframe3]
        layouts = [hlayout1, hlayout2, hlayout3]
        self.layout.addWidget(hframe1)
        self.layout.addWidget(hframe2)
        self.layout.addWidget(hframe3)

        self.layout.addWidget(QLabel('IN4 - Vetor t'))
        self.entrys = [e1, e2, e3]
        for entry in self.entrys:
            entry.textEdited.connect(self.node.updateNode)

        hframe_out = QFrame()
        hlayout_out = QHBoxLayout(hframe_out)

        svg_out = SVGLabel().load('A sin(2\pi f t + \phi)', size=(100, 20))

        hlayout_out.setAlignment(Qt.AlignLeft)
        hlayout_out.addWidget(svg_out)

        self.layout.addWidget(hframe_out)
    def refresh(self):
        entrySockets = [{'socket': self.node.inputs[0], 'entry': self.entrys[0]},
                        {'socket': self.node.inputs[1], 'entry': self.entrys[1]},
                        {'socket': self.node.inputs[2], 'entry': self.entrys[2]}]

        data = self.node.checkConnectedEdgeData(entrySockets)


        if (self.node.inputs[3].hasEdge() and self.node.outputs[0].hasEdge()):
            t = self.node.inputs[3].edge.data

            A = float(data[0])
            f = float(data[1])
            phase = float(data[2])
            seno = A * np.sin(2 * np.pi * f * t + phase)
            try:
                self.node.sendSignal([seno], [self.node.outputs[0]], [self], ['float'])
            except TypeError:
                logging.error('Verifique se o valor pode ser convertido para número')


class QDMNodeSignalImpulse(QWidget):
    def __init__(self, node, parent = None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        mainFrame = QFrame()
        mainLayout = QVBoxLayout()
        mainFrame.setLayout(mainLayout)

        mainLayout.addWidget(QLabel('Vetor t'))
        l1 = QLabel('Duração - [s]')
        e1 = QLineEdit()
        e1.textEdited.connect(self.node.updateNode)

        hframe = QFrame()
        hlayout = QHBoxLayout()
        hlayout.addWidget(l1)
        hlayout.addWidget(e1)
        hframe.setLayout(hlayout)


        self.entrys = [e1]
        mainLayout.addWidget(hframe)
        self.selectedWidgetFrame = QFrame()
        self.selectedWidgetLayout = QVBoxLayout()
        self.selectedWidgetFrame.setLayout(self.selectedWidgetLayout)

        mainLayout.addWidget(self.selectedWidgetFrame)
        self.layout.addWidget(mainFrame)

    def refresh(self):
        entrySocket = [{'socket': self.node.inputs[1], 'entry': self.entrys[0]}]

        dados = self.node.checkConnectedEdgeData(entrySocket)

        if self.node.inputs[0].hasSignal():

            t = self.node.inputs[0].edge.data
            N = len(t)

            if (not None in dados and dados[0]!=''):
                periodo = float(dados[0])
                pulse = np.sin(1/periodo*np.pi*t)
                pulse[t >= periodo] = 0

                self.node.sendSignal([pulse], [self.node.outputs[0]], [self], ['float'])