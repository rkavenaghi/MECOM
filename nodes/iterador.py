from core.node import *
from core.node_socket import *




class Node_iterador(Node):
    def __init__(self, scene, title="Iterador 1D", parent=None, method=None):
        super().__init__(Node=self)
        self.MODULO = 'Iterador'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = title

        self.content = QDMNodeIterador(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(200, 100)

        self.grNode.initUI()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [{'pos': 0.55, 'type': 'float'}, {'pos': 0.78, 'type': 'int'}]
        outputs = [{'pos': 0.78, 'type': 'float'}]

        self.inputs = []
        self.outputs = []
        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

class QDMNodeIterador(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(QGridLayout())
        l1 = QLabel('Vetor')
        l2 = QLabel('Índice')
        l3 = QLabel('Vetor[Índice]')

        self.layout().addWidget(l1, 0, 0)
        self.layout().addWidget(l2, 1, 0)
        self.layout().addWidget(l3, 1, 1)

    def getIndex(self):
        if self.node.inputs[1].hasSignal():
            edge = self.node.inputs[1].edge
            signal = edge.data
            if isinstance(signal, float):
                if signal.is_integer():
                    index = int(signal)
                    if self.node.inputs[0].hasSignal():
                        edge = self.node.inputs[0].edge
                        data = edge.data
                        try:
                            self.node.sendSignal([data[index]], [self.node.outputs[0]], [self], ['float'])
                        except IndexError:
                            logging.error(f'Indice {index} não presente')
                else:
                    self.node.invalidSignal()


    def refresh(self):
        self.getIndex()