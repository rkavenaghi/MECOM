from core.node import *
from core.node_socket import *
class Node_function(Node):
    def __init__(self, scene, title="Função", parent=None, method=None):
        super().__init__(Node=self)
        self.MODULO = 'Função'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = title

        self.content = QDMNodeFunction(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(400, 240)

        self.grNode.initUI()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [{'pos': 0.4, 'type': 'float'}, {'pos': 0.6, 'type': 'int'}]
        outputs = [{'pos': 0.8, 'type': 'undefined'}]

        self.inputs = []
        self.outputs = []
        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()


class QDMNodeFunction(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(QGridLayout())
        l1 = QLabel('*args')
        l2 = QLabel('**kwargs')
        l3 = QLabel('output')

        plainText_1 = QTextEdit()
        plainText_1.textChanged.connect(self.node.updateNode)
        self.plainText = [plainText_1]



        self.layout().addWidget(l1, 0, 0)
        self.layout().addWidget(l2, 1, 0)
        self.layout().addWidget(l3, 2, 1)
        self.layout().addWidget(plainText_1, 3, 0, 3, 2)



    def refresh(self):

        text = self.plainText[0].toPlainText()
        try:

            logging.info(exec(text))
        except SyntaxError:
            logging.error('Digite código Python válido')
        except Exception as error:
            print(error)
