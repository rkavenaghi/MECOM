from core.node import *
import numpy as np

DEBUG = True
import logging

NO_MODE = 0
GET_ROW = 1
GET_COLUMN = 2
TRANSPOR = 3


class Node_array(Node):


    def __init__(self, scene, title="Vetor 1D", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Vetor'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.method = method
        self.title = title
        self.content = QDMNodeArray(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(280, 240)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [{'pos': 0.23, 'type': 'float', 'label': 'Mínimo git rm do intervalo', 'multiple_edges': False},
                  {'pos': 0.36, 'type': 'float', 'label': 'Máximo do intervalo', 'multiple_edges': False},
                  {'pos': 0.49, 'type': 'int', 'label': 'Número de pontos', 'multiple_edges': False}]

        outputs = [{'pos': 0.68, 'type': 'float', 'label': 'Vetor 1D'},
                   {'pos': 0.88, 'type': 'float', 'label': 'Período'}]

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

class QDMNodeArray(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def refresh(self):

        try:
            y, dt = self.resultant()
            self.node.sendSignal([y, dt], self.node.outputs, [self, self], ['float', 'float'])
        except TypeError:
            logging.error('Digite um número nas entradas')

    def resultant(self):

        entrySocket = [{'socket': self.node.inputs[0], 'entry': self.entrys[0]},
                       {'socket': self.node.inputs[1], 'entry': self.entrys[1]},
                       {'socket': self.node.inputs[2], 'entry': self.entrys[2]}]

        dados = self.node.checkConnectedEdgeData(entrySocket)


        try:
            if not None in dados:
                p1, p2, p3 = dados
                y, dt = np.linspace(float(p1), float(p2), int(p3), retstep=True)

            return y, dt
        except Exception as error:
            logging.error('Valores nao corretos em nodes.array')
            self.node.invalidSignal()

    def initUI(self):

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        e1 = QLineEdit()
        e1.textEdited.connect(self.node.updateNode)
        e2 = QLineEdit()
        e2.textEdited.connect(self.node.updateNode)
        e3 = QLineEdit()
        e3.textEdited.connect(self.node.updateNode)
        l1 = QLabel('IN1 - Início')
        l2 = QLabel('IN2 - Fim')
        l3 = QLabel('IN3 - Número de Pontos')

        self.entrys = [e1, e2, e3]
        layout = QGridLayout()
        layout.addWidget(l1, 0, 0)
        layout.addWidget(e1, 0, 1)
        layout.addWidget(l2, 1, 0)
        layout.addWidget(e2, 1, 1)
        layout.addWidget(l3, 2, 0)
        layout.addWidget(e3, 2, 1)
        option = QFrame()
        option.setLayout(layout)

        self.layout.addWidget(option)
        self.layout.addWidget(QLabel('OUT1 - Vetor'))
        self.layout.addWidget(QLabel('OUT2 - Período'))
