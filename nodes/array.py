from core.node import *
import numpy as np


DEBUG = True
import logging


NO_MODE = 0
GET_ROW = 1
GET_COLUMN = 2
TRANSPOR = 3

class Node_array(Node):
    """
    Nó para criar numpy.arrays utilizando os métodos numpy.arange e numpy.linspace.

    DOCUMENTAÇÃO:
        MÓDULO: Vetor
        MÉTODO: -

    RESUMO:
    Nó utilizado para gerar arrays unidimensionais.


    INPUTS:
        - aresta 1:
        - aresta 2:
    OUTPUTS:
        - aresta 1: 
        - aresta 2:
    


    """
    # TODO Corrigir entrys e input edges no codigo.

    def __init__(self, scene, title="Vetor 1D", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Vetor'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent

        self.method = method

        if method == 'Vetor':
            self.title = 'Tensor O1'
            self.content = QDMNodeArray(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(280, 240)
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            inputs = [{'pos': 0.43, 'type': 'float'},
                      {'pos': 0.56, 'type': 'float'},
                      {'pos': 0.69, 'type': 'int'}]

            outputs = [{'pos': 0.8, 'type': 'float'},
                       {'pos': 0.9, 'type': 'float'}]

            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()


        elif method == 'Matriz':
            self.title = 'Tensor O2'
            self.content = QDMNodeMatriz(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(280, 200)
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            inputs = [{'pos': 0.15, 'type' : 'float'},
                      {'pos': 0.40, 'type' : 'int'}]
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

    MODE = 'NO_MDOE'
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
                self.node.sendSignal([np.array(self.node.inputs[0].edge.data).T], [self.node.outputs[0]], [self], ['float'])
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



class QDMNodeArray(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()
        
    def refresh(self):
        for radiobutton in self.radio_buttons:
            if radiobutton.isChecked():
                self.selected_button = radiobutton
                break

        if self.selected_button.text() == 'arange':
            self.options_radio['l3'].setText('IN3 - Passo')
            self.node.inputs[2].setColor('float')
        elif self.selected_button.text() == 'linspace':
            self.options_radio['l3'].setText('IN3 - Número de Pontos')
            self.node.inputs[2].setColor('int')

        try:
            y, dt = self.resultant()
            self.node.sendSignal([y, dt], self.node.outputs, [self, self], ['float', 'float'])
        except TypeError:
            logging.error('Digite um número nas entradas')


    def resultant(self):

        entrySocket = [{'socket': self.node.inputs[0], 'entry':self.entrys[0]},
                       {'socket': self.node.inputs[1], 'entry':self.entrys[1]},
                       {'socket': self.node.inputs[2], 'entry':self.entrys[2]}]

        dados = self.node.checkConnectedEdgeData(entrySocket)

        try:
            if not None in dados:
                p1, p2, p3 = dados
            if self.selected_button.text() == 'linspace':
                y, T = np.linspace(float(p1), float(p2), int(p3), retstep=True)
            elif self.selected_button.text() == 'arange':

                y = np.arange(float(p1), float(p2), float(p3))
                T = len(y)
            return y, T
        except Exception as error:
            logging.error('Valores nao corretos em nodes.array')
            self.node.invalidSignal()


    def initUI(self):
        # CADA INPUT DO SISTEMA DEVE ESTAR ASSOCIADO A UM SOCKET


        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0,0,0,0)


        self.frame_radio = QFrame()
        self.layout_radio = QHBoxLayout()


        options = ['linspace', 'arange']
        self.radio_buttons = [QRadioButton(options[0]), QRadioButton(options[1])]
        self.radio_buttons[0].setChecked(True)
        for opcao, radiobutton in zip(options, self.radio_buttons):

            radiobutton.toggled.connect(self.refresh)
            self.layout_radio.addWidget(radiobutton)



        self.frame_radio.setLayout(self.layout_radio)
        self.layout.addWidget(self.frame_radio)

        e1 = QLineEdit()
        e1.textEdited.connect(self.node.updateNode)
        e2 = QLineEdit()
        e2.textEdited.connect(self.node.updateNode)
        e3 = QLineEdit()
        e3.textEdited.connect(self.node.updateNode)
        l1 =QLabel('IN1 - Início')
        l2 = QLabel('IN2 - Fim')
        l3 = QLabel('IN3 - Número de Pontos')
        self.options_radio = {'l1':l1, 'l2':l3, 'l3':l3, 'e1':e1, 'e2':e2, 'e3':e3}


        self.entrys=[e1,e2,e3]
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
