from core.node import *
import numpy as np

DEBUG = True
import logging

NO_MODE = 0
GET_ROW = 1
GET_COLUMN = 2
TRANSPOR = 3


class Node_matrix(Node):


    def __init__(self, scene, parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Matriz'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = 'Tensor O2'
        self.content = QDMNodeMatriz(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(280, 340)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [{'pos': 0.15, 'type': 'float'},
                  {'pos': 0.40, 'type': 'int'}]
        outputs = [{'pos': 0.5, 'type': 'float'}]

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

        try:
            mode = self.kwargs['MODE']
        except:
            return

        if mode == GET_ROW:
            self.content.comboBox.setCurrentIndex(1)
        elif mode == GET_COLUMN:
            self.content.comboBox.setCurrentIndex(2)
        elif mode == TRANSPOR:
            self.content.comboBox.setCurrentIndex(3)


class QDMNodeMatriz(QWidget):
    MODE = 'NO_MODE'

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.comboBox = QComboBox()

        self.comboBox.addItem('Selecione uma função')
        self.comboBox.addItem('Extrair Linhas')
        self.comboBox.addItem('Extrair Coluna')
        self.comboBox.addItem('Extrair Coeficiente')
        self.comboBox.addItem('Transpor')
        self.comboBox.currentIndexChanged.connect(self.escolhaFuncao)

        self.function_frame = QFrame()
        self.function_frame.setFixedSize(200, 200)
        self.function_layout = QVBoxLayout()
        self.function_frame.setLayout(self.function_layout)

        self.layout.addWidget(QLabel('IN1 - Matriz'))

        self.layout.addWidget(self.comboBox)
        self.layout.addWidget(self.function_frame)

    def escolhaFuncao(self):
        funcao = self.sender().currentText()
        while self.function_layout.takeAt(0):
            pass

        if funcao == 'Extrair Linhas':
            self.MODE = GET_ROW
            hframe = QFrame()
            hlayout = QHBoxLayout(hframe)

            self.entrys = [QLineEdit()]
            hlayout.addWidget(QLabel('Linhas'))
            hlayout.addWidget(self.entrys[0])

            self.function_layout.addWidget(hframe)

            for entry in self.entrys:
                entry.textEdited.connect(self.node.updateNode)
        elif funcao == 'Extrair Coluna':
            self.MODE = GET_COLUMN

            self.function_layout.addWidget(QLabel('teste 1'))

        elif funcao == 'Transpor':
            self.MODE = TRANSPOR
            if self.node.inputs[0].hasSignal():
                self.node.sendSignal([np.array(self.node.inputs[0].edge.data).T], [self.node.outputs[0]], [self],
                                     ['float'])
        else:
            logging.warning('Funcao nao implementada')

        self.node.kwargs.update({'MODE': self.MODE})

    def refresh(self):
        if self.MODE == GET_ROW:
            try:
                data = self.node.inputs[0].edge.data if self.node.inputs[0].hasSignal() else None
                entrySocket = [{'socket': self.node.inputs[1], 'entry': self.entrys[0]}]
                dados = self.node.checkConnectedEdgeData(entrySocket)[0]

                mask = [int(value) for value in dados.split(',')] if ',' in dados else int(dados)
                self.node.sendSignal([np.array(data)[mask]], self.node.outputs, [self], ['float'])

            except ValueError:
                logging.error('Escreve um número que possa ser convertido para inteiro')

            except IndexError:
                logging.error('Indíce não existe')

