from core.node import *
import numpy as np
import logging

class Node_scalar(Node):

    def __init__(self, scene, title="Variável", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Variável'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.method = method
        self.title = title
        self.content = QDMNodeScalar(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(240, 180)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = []
        outputs = [{'pos': 0.81, 'type': 'float', 'label': 'Escalar'}]

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()


class QDMNodeScalar(QWidget):
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()
        self.data = None

    def updateDisplayText(self):
        try:
            self.svg_widget.load(self.display.text() + '=' + self.output_label.text(), fontsize=12, color='#f0f0f0')
            self.svg_widget.adjustSize()
        except ValueError:
            pass
    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        self.entry = LineEntryEdit('Valor')

        self.display = QLineEdit('Display')
        self.alias = QLineEdit('Alias')
        self.svg_widget = SVGLabel()
        self.svg_widget.load(self.display.text(), color='#f0f0f0')

        self.svg_widget.adjustSize()
        self.output_label = QLabel(' ')
        self.display.textChanged.connect(self.updateDisplayText)


        self.entry.textChanged.connect(self.node.updateNode)


        self.layout.addWidget(self.display, 0, 1)
        self.layout.addWidget(QLabel('Display'), 0, 0)
        self.layout.addWidget(self.alias, 1, 1)
        self.layout.addWidget(QLabel('Alias'), 1, 0)
        self.layout.addWidget(self.entry, 2, 1)
        self.layout.addWidget(QLabel('Expressão'), 2, 0)

        self.layout.addWidget(self.svg_widget, 3, 0, 1, 2)
        #self.layout.addWidget(self.output_label, 4, 0, 1, 2)
        self.entrys = [self.entry, self.display, self.alias]
        self.node.parent.variables.append(self.node)

    def refresh(self):

        value = self.entry.text()
        readdata = self.entry.evaluate(value)
        try:
            self.output_label.setText(f'{readdata:.3e}')
        except ValueError:
            self.output_label.setText(f'---')
        self.updateDisplayText()

        self.data = readdata
        if (self.node.outputs[0].hasEdge()):
            self.node.sendSignal([self.data], self.node.outputs, [self], ['float'])

