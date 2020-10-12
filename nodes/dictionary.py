from core.node import *
import numpy as np

DEBUG = True
import logging

class Node_dictionary(Node):

    # TODO Corrigir entrys e input edges no codigo.

    def __init__(self, scene, title="Dicionário", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Dicionário'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.method = method
        self.title = title
        self.content = QDMNodeDict(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(200, 120)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)


        inputs = [{'pos': 0.5, 'type': 'dict'}]
        outputs = [{'pos': 0.5, 'type': 'undefined'}]

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

        if 'INDEX' in self.kwargs.keys():
            self.content.comboBox.setCurrentIndex(self.kwargs['INDEX'])


class QDMNodeDict(QWidget):
    DICT_INDEX = 0

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def refresh(self):
        self.updateKeys()
        self.getDataFromDict()

    def initUI(self):

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(QLabel('IN1 - Dicionário'))
        self.comboBox = QComboBox()
        self.comboBox.currentIndexChanged.connect(self.node.updateNode)
        self.comboBox.addItem('Selecione a chave')

        self.layout.addWidget(self.comboBox)

    def getDataFromDict(self):
        self.DICT_INDEX = self.comboBox.currentIndex()
        self.node.kwargs.update({'INDEX': self.DICT_INDEX})
        try:

            if (self.node.outputs[0].hasEdge() and self.DICT_INDEX!=0):
                key = self.comboBox.currentText()

                data = self.inputDictionary[key]
                self.node.sendSignal([data],
                                     self.node.outputs,
                                     [self],
                                     ['float'])#Float talvez

        except AttributeError as error:
            logging.error(error)



    def updateKeys(self):
        if self.node.inputs[0].hasSignal():
            self.inputDictionary = self.node.inputs[0].edge.data

            if self.comboBox.count() == 1: #Nao foram adicionados os itens
                for cont, item in enumerate(self.inputDictionary):
                    self.comboBox.addItem(item)
                return

            elif self.comboBox.count() < len(self.inputDictionary) + 1:  #Resetar os itens
                for cont in range(1, self.comboBox.count()):
                    self.comboBox.removeItem(0)
                self.updateKeys()
                return





