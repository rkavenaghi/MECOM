from core.node import *
from core.node_socket import *

DEBUG = True


class Node_string(Node):
    def __init__(self, scene, title="Diretório", parent=None, method=None):
        super().__init__(Node=self)
        self.MODULO = 'Diretório'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = title

        self.content = QDMNodeString(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(200, 120)
        self.grNode.initUI()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = []
        outputs = [{'pos': 0.75, 'type': 'str'}]

        self.inputs = []
        self.outputs = []

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()


class QDMNodeString(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        mainLayout = QVBoxLayout()
        l1 = QLabel('Digite o caminho')
        e1 = QLineEdit()
        e1.setText(__file__)
        e1.textEdited.connect(self.node.updateNode)

        self.entrys = [e1]
        mainLayout.addWidget(l1)
        mainLayout.addWidget(e1)
        self.setLayout(mainLayout)

    def getText(self):
        text = self.entrys[0].text()
        return text

    def refresh(self):
        text = self.getText()
        self.node.sendSignal([text], [self.node.outputs[0]], [self], ['str'])