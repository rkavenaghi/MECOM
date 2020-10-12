from core.node import *
from PyQt5.QtWidgets import QWidget
import numpy as np

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4
SINGLEPLOT = 0
MULTIPLEPLOT = 1

import pyqtgraph as pg

class Node_graphics(Node):

    
    def __init__(self,scene,title="Visualização 2D",parent=None, method=None, *args, **kwargs):
        super().__init__(Node=self, *args, **kwargs)
        self.MODULO = 'Gráfico'
        self.MODULO_INITIALIZED = False #Parametro utilizado para nomear nas arvores de objetos
        self.parent = parent
        self.scene = scene
        self.title = title
        inputs = [{'pos': 0.84, 'type': 'float'},
                  {'pos': 0.88, 'type': 'float'},
                  {'pos': 0.94, 'type': 'str'}]
        outputs = []

        self.content = QDMNodeGraphics(self) 
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(480, 550)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)
        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

        # if 'plot_title' in self.kwargs.keys():
        #     self.content.ax.set_title(kwargs['plot_title'])
        # if 'x_label_text' in self.kwargs.keys():
        #     self.content.ax.set_xlabel(kwargs['x_label_text'])
        # if 'y_label_text' in self.kwargs.keys():
        #     self.content.ax.set_ylabel(kwargs['y_label_text'])
        # self.content.figure.tight_layout()

class QDMNodeGraphics(QWidget):

    savefile_extension = 'png'
    data_line = None

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setContentsMargins(5, 5, 5, 5)
        self.canvas = pg.PlotWidget()


        self.layout.addWidget(self.canvas, 0, 0, 3, 3)

        save_label = QLabel('Salvar em')
        self.entrys = [QLineEdit()]

        self.layout.addWidget(QLabel('X'), 3, 0)
        self.layout.addWidget(QLabel('Y'), 4, 0)

        self.layout.addWidget(QLabel('Extensão'), 5, 0)
        self.layout.addWidget(self.entrys[0], 5, 1)

        self.comboBoxExtension = QComboBox()
        self.comboBoxExtension.addItem('png')
        self.comboBoxExtension.setCurrentIndex(0)
        self.comboBoxExtension.currentIndexChanged.connect(self.selectExtension)
        self.layout.addWidget(self.comboBoxExtension, 5, 2)



    def refresh(self):
        try:
            if (self.node.inputs[0].hasSignal() and self.node.inputs[1].hasSignal()):
                logging.info('Atualizar gráfico')
                x_data = self.node.inputs[0].edge.data
                y_data = self.node.inputs[1].edge.data



                try:
                    n_xplots = x_data.shape[1]
                    self.MODE = MULTIPLEPLOT
                    shapes_match = True if (
                                x_data.shape == y_data.shape) else False
                except IndexError:
                    self.MODE = SINGLEPLOT
                    shapes_match = True if x_data.shape[0] == y_data.shape[0] else False
                else:
                    shapes_match = False

                if (self.MODE == SINGLEPLOT and shapes_match):
                    self.data_line = self.canvas.plot(x_data, y_data) if isinstance(self.data_line, type(None)) else self.updateLine(x_data, y_data)

        except Exception as error:
            print(error)
            raise Exception

    def updateLine(self, x, y):
        self.data_line.setData(x, y)
        return self.data_line

        # if prosseguir:
        #     entrySocket = [{'socket': self.node.inputs[2], 'entry': self.entrys[0]}]
        #     diretorio_save = self.node.checkConnectedEdgeData(entrySocket)[0]
        #
        #     savefile = 1 if diretorio_save!='' else 0
        #     if (savefile and prosseguir):
        #         logging.info(f'Salvando figura em: {diretorio_save}')
        #         self.figure.savefig(diretorio_save, format=self.savefile_extension)


    def selectExtension(self):
        self.savefile_extension = self.comboBoxExtension.currentText()
        logging.info(f'Extensão modificada para {self.savefile_extension}')

