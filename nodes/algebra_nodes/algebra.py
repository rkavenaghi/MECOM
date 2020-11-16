import numpy as np

from core.node import *
from core.node_socket import *
from utils.MECWidgets import SVGLabel
import logging

from .somatorio_node import QDMNodeAlgebraSoma

class Node_algebra(Node):
    """ Módulo contendo operadores lineares.

    Métodos a serem implementados:
    - Multiplicação por escalar(Divisão)

    Métodos implementados:
    - Adição (Subtração)
    - Convolução

    Entradas: 2 vetores.
    Saída: 1 vetor.

    """
    def __init__(self, scene, title="Álgebra", parent=None, method = None, data_type='float'):
        super().__init__(Node = self)
        self.data_type=data_type
        self.method = method
        self.scene = scene
        self.parent = parent
        self.MODULO_INITIALIZED = False

        self.title = method
        self.MODULO = method
        prosseguir = False

        if method == 'Convolução':

            self.content = QDMNodeAlgebraConvolucao(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(320, 180)
            inputs = [0.26, 0.38, 0.53]
            outputs = [0.8]
            prosseguir = True
        elif method == 'Produto':
            self.content = QDMNodeAlgebraProduto(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(200, 120)
            inputs = [0.35]
            outputs = [0.8]
            prosseguir = True

        elif method == 'Inversa':
            self.content = QDMNodeAlgebraDivisao(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.width = 160
            self.grNode.height = 180
            self.grNode.initUI()
            inputs = [0.38]
            outputs = [0.8]
            prosseguir = True


        else:
            logging.error('Não implementado ainda')
            prosseguir = False
        if prosseguir:
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            self.inputs = []
            self.outputs = []
            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()



class QDMNodeAlgebraDivisao(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        hframe1 = QFrame()
        hlayot1 = QHBoxLayout(hframe1)

        label = QLabel('IN1: ')
        hlayot1.addWidget(label)

        svg_w1 = SVGLabel()
        svg_w1.load('x', fontsize=16, color='#f0f0f0', size=(30, 30))
        hlayot1.addWidget(svg_w1)


        label2 = QLabel('OUT2: ')
        hframe = QFrame()
        hlayot = QHBoxLayout()
        hframe.setLayout(hlayot)

        svg_widget = SVGLabel()
        svg_widget.load('\dfrac{1}{x}', fontsize=16, color='#f0f0f0', size=(30, 30))
        self.layout.addWidget(hframe1)

        hlayot.addWidget(label2)
        hlayot.addWidget(svg_widget)
        self.layout.addWidget(hframe)
    def refresh(self):

        if self.node.inputs[0].hasEdge():
            if not isinstance(self.node.inputs[0].edge.data, type(None)):
                data = 1/self.node.inputs[0].edge.data
                try:
                    self.node.sendSignal([data], [self.node.outputs[0]], [self], ['float'])

                except:
                    logging.warning('Erro em Divisão ')
                    self.node.invalidSignal()





class QDMNodeAlgebraConvolucao(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        label0 = SVGLabel().load('\Delta t', size=(25, 25))
        label = QLabel('IN2 - Vetor 1')
        label2 = QLabel('IN3 - Vetor 2')

        label3 = QLabel('OUT2 - ')
        hframe = QFrame()
        hlayot = QHBoxLayout()
        hframe.setLayout(hlayot)



        svg_widget = SVGLabel()
        svg_widget.load('(x * y)[n] = \Delta t \sum_{m=-\infty}^{\infty} x[m]y[n - m]', fontsize=16, color='#f0f0f0')

        svg_widget.setFixedWidth(210)
        svg_widget.setFixedHeight(40)

        self.layout.addWidget(label0)
        self.layout.addWidget(label)
        self.layout.addWidget(label2)
        hlayot.addWidget(label3)
        hlayot.addWidget(svg_widget)
        self.layout.addWidget(hframe)

    def convolve(self):
        """
        Funcionar apenas com 1 edge em cada socket.
        """
        prosseguir = False
        edgedata = []
        for inputsocket in self.node.inputs[1:]:
            if inputsocket.hasEdge():

                if not isinstance(inputsocket.edge.data, type(None)):
                    edgedata.append(inputsocket.edge.data)
                    prosseguir = True

        if prosseguir:
            samelength = [len(_x) == len(edgedata[0]) for _x in edgedata]
            N = len(edgedata[0])
            if (samelength and len(edgedata)==2):
                dt = self.node.inputs[0].edge.data
                convolved_array = dt*np.convolve(*edgedata, mode='full')[:N]
                return convolved_array
            else:
                logging.warning('Elementos de tamanhos diferentes')
                return None

    def refresh(self):
        value = self.convolve()
        if not isinstance(value, type(None)):
            for outputs in self.node.outputs:
                for edge in outputs.edges:

                    edge.signal(value, self, 'float')
        else:
            for outputs in self.node.outputs:
                for edge in outputs.edges:
                    edge.signal(None, self)



class QDMNodeAlgebraProduto(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        label = QLabel('IN1 - Escalares e Vetores')
        label2 = QLabel('OUT2 - ')
        hframe = QFrame()
        hlayot = QHBoxLayout()
        hframe.setLayout(hlayot)

        svg_widget = SVGLabel()
        svg_widget.load('x[k] = \prod_{k=0}^{M}a_k \prod_{j=0}^{N}x_j[k]', fontsize=16, color='#f0f0f0')
        svg_widget.setFixedWidth(100)
        svg_widget.setFixedHeight(40)

        self.layout.addWidget(label)

        hlayot.addWidget(label2)
        hlayot.addWidget(svg_widget)
        self.layout.addWidget(hframe)

    def refresh(self):
        """
        As entradas podem ser escalares ou vetoriais
        """


        edgedata = []
        for inputsocket in self.node.inputs:
            if inputsocket.hasEdge():
                for edge in inputsocket.edges:
                    if not isinstance(edge.data, type(None)):
                        edgedata.append(edge.data)

        maskScalar = [(type(value) == float or type(value) == int) for value in edgedata]
        maskArray = [not boolean for boolean in maskScalar]


        constants = np.array(edgedata)[maskScalar]
        constants_product = 1
        for value in constants: constants_product *= value
        arrays = np.array(edgedata)[maskArray]
        samelength = [(len(_x) == len(arrays[0])) for _x in arrays]

        if (samelength):
            output = constants_product*np.prod([*arrays], axis=0)
            self.node.sendSignal([output], [self.node.outputs[0]],[self], ['float'])





