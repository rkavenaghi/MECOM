from core.node import *
import numpy as np

DEBUG = True
import logging

NO_MODE = 0
GET_ROW = 1
GET_COLUMN = 2
TRANSPOR = 3


class Node_somatorio(Node):

    def __init__(self, scene, title="Soma", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Soma'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.method = method
        self.title = title
        self.content = QDMNodeAlgebraSoma(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(100, 120)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [{'pos': 0.42, 'type': 'float', 'label': 'Soma +', 'multiple_edges': True},
                  {'pos': 0.8, 'type': 'float', 'label': 'Soma -', 'multiple_edges': True}]
        outputs = [{'pos': 0.8, 'type': 'float', 'label': 'Soma saída', 'multiple_edges': True}]

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()


class QDMNodeAlgebraSoma(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        label1 = QLabel('IN +')
        label2 = QLabel('IN -')
        label3 = QLabel('OUT')

        self.layout.addWidget(label1, 0, 0)
        self.layout.addWidget(label2, 1, 0)
        self.layout.addWidget(label3, 1, 1)

    def refresh(self):
        soma = 0
        if self.node.inputs[0].hasSignal():
            for edge in self.node.inputs[0].edges:
                soma += edge.data
        if self.node.inputs[1].hasSignal():
            for edge in self.node.inputs[1].edges:
                soma -= edge.data

        print(soma)

        for edge in self.node.outputs[0].edges:
            edge.signal(soma, self, 'float')

    #     for inputsocket in self.node.inputs:
    #         if inputsocket.hasEdge():
    #             for edge in inputsocket.edges:
    #                 if edge.hasSignal():
    #                     edgedata.append(edge.data)
    #
    #     if samelength:
    #         # Funciona tanto para listas quanto para arrays.
    #         return np.array([sum(i) for i in zip(*edgedata)])
    #     else:
    #         logging.warning('Elementos de tamanhos diferentes')
    #         return None
    #
    # def refresh(self):
    #     value = self.add()
    #     if not isinstance(value, type(None)):
    #         for outputs in self.node.outputs:
    #             for edge in outputs.edges:
    #
    #                 edge.signal(value, self, 'float')
    #     else:
    #         for outputs in self.node.outputs:
    #             for edge in outputs.edges:
    #                 edge.signal(None, self)
