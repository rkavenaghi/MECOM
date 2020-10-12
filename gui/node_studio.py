from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QFile, QSaveFile
from PyQt5.Qt import QMainWindow
from core import scene
from core.node import Node, QDMGraphicsNode
import importlib


import sys
class Studio(QMainWindow):
    node = []
    node_width = 300
    node_height = 300
    node_title = 'Título - No_custom'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setGeometry(0, 0, 1200, 600)
        self.setWindowTitle('Estúdio para Criação de Nós')
        self.stylesheet_filename= '../configurations/qss/nodestyle.qss'
        self.loadStylesheet(self.stylesheet_filename)
        self.mainWidget = QWidget(self)
        self.layout = QGridLayout(self.mainWidget)
        self.setCentralWidget(self.mainWidget)

        self.view = QGraphicsView(self)
        self.scene = scene.Scene(parent=self)


        test_button = QPushButton('Testar - [F5]')
        test_button.setShortcut('F5')
        title_button = QLineEdit('Título - No_custom')
        title_button.textChanged.connect(self.change_title)

        test_button.clicked.connect(self.run_node)

        frame = QFrame()
        frame.setFixedWidth(300)
        frame.setFixedHeight(40)
        layout = QHBoxLayout(frame)


        label_dimensoes = QLabel('Dimensões (w,h)')
        entry_dimensoes_1 = QLineEdit()
        entry_dimensoes_1.textChanged.connect(self.width_change)
        entry_dimensoes_2 = QLineEdit()
        entry_dimensoes_1.textChanged.connect(self.height_change)

        layout.addWidget(label_dimensoes)
        layout.addWidget(entry_dimensoes_1)
        layout.addWidget(entry_dimensoes_2)

        self.layout.addWidget(self.view, 0, 0, 10, 1)
        self.layout.addWidget(test_button, 0, 1)
        self.layout.addWidget(title_button, 1, 1)
        self.layout.addWidget(frame, 2, 1)

        self.view.setScene(self.scene.grScene)

        self.show()

    def change_title(self):
        self.node_title = self.sender().text()

    def width_change(self):
        width_val = self.sender().text()
        try:
            width = int(width_val)
            self.node_width = width
        except ValueError as error:
            print(error)
    def height_change(self):
        height_val = self.sender().text()
        try:
            height = int(height_val)
            self.node_height = height
        except ValueError as error:
            print(error)



    def run_node(self):
        for nodes in self.node:
            self.scene.removeNode(nodes)
        class Node_custom(Node):
            def __init__(self, scene,title="Módulo Customizado", parent=None, method=None, *args, **kwargs):

                self.constructor = kwargs['constructor']

                self.scene = scene
                self.title = self.constructor.node_title
                self.parent = parent
                self.method = method

                self.content = QDMNodeCustom(self)
                self.grNode = QDMGraphicsNode(self)

                print(self.constructor.node_width)
                print(self.constructor.node_height)
                self.grNode.resize(self.constructor.node_width, self.constructor.node_height)


                inputs = []
                outputs = []

                self.scene.addNode(self)
                self.scene.grScene.addItem(self.grNode)
                self.configInputsOutputs(inputs, outputs)

        class QDMNodeCustom(QWidget):
            def __init__(self, node, parent=None):
                super().__init__(parent)
                self.node = node
                self.initUI()

            def initUI(self):
                self.layout = QVBoxLayout()
                self.layout.setContentsMargins(0, 0, 0, 0)
                self.setLayout(self.layout)

        self.node.append(Node_custom(self.scene, constructor=self))



    def loadStylesheet(self, filename):
        file = QFile(filename)
        file.open(QFile.ReadOnly | QFile.Text)
        stylesheet = file.readAll()
        QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))





def run_studio():
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    window = Studio()
    sys.exit(app.exec_())
if __name__ == "__main__":
    run_studio()