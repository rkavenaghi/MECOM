from core.node import *


DEBUG = True
import logging

class Node_group(Node):

    def __init__(self, scene, nodes, input_sockets, output_sockets, title="Grupo", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Grupo'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.method = method
        self.title = 'Grupo'

        self.content = QDMNodeGroup(self)
        self.grNode = QDMGraphicsNode(self)

        n_i = len(input_sockets)
        n_o = len(output_sockets)

        padding = 40
        sockets_spacing = 30

        node_height = sockets_spacing*(max([n_i, n_o]) - 1) + 2*padding

        self.grNode.resize(400, node_height)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [{'pos':  (padding+sockets_spacing*cont)/node_height,
                   'type': socket.data_type,
                   'label': socket.label} for cont, socket in enumerate(input_sockets)]

        outputs = [{'pos': (padding+sockets_spacing*cont)/node_height,
                   'type': socket.data_type,
                    'label': socket.label} for cont, socket in enumerate(output_sockets)]

        #TODO implementar etiquetas para todos os sockets, dessa forma será possível identificar cada socket

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

        self.content.initUI()


class QDMNodeGroup(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)


    def refresh(self):
        pass

    def initUI(self):
        # CADA INPUT DO SISTEMA DEVE ESTAR ASSOCIADO A UM SOCKET

        self.layout = QGridLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        self.frame = QFrame()

        for cont, input_socket in enumerate(self.node.inputs):
            print(input_socket.label)
            self.layout.addWidget(QLabel(input_socket.label), cont, 0)

        for cont, output_socket in enumerate(self.node.outputs):
            print(output_socket.label)
            self.layout.addWidget(QLabel(output_socket.label), cont, 1)
