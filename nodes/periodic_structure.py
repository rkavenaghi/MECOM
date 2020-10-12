from core.node import *
from PyQt5.QtWidgets import QWidget

class Node_periodic(Node):
    def __init__(self, scene, title="Sem nome", parent=None, method=None):
        super().__init__(Node=self)
        self.MODULO = 'Estruturas Periódicas'
        self.MODULO_INITIALIZED = False
        self.parent = parent
        self.scene = scene
        self.title = title

        self.content = QDMNodePeriodic(self)  # mando o node tambem
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(800, 600)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.configInputsOutputs()



        self.configureObjectTree()

    def updateNode(self):
        self.content.result_calculation()
        super().propagate()

class QDMNodePeriodic(QWidget):
    def __init__(self, node, parent=None):
        super().__init__()
        self.node = node
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.layout.addWidget(QLabel('Projeto de Estruturas Periódicas'))


def run():
    print('Pacote de Estruturas Periódicas')

if __name__ == '__main__':
    run()