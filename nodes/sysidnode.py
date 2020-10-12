
import numpy as np
from core.node import *
from core.node_socket import *
from utils.MECWidgets import SVGLabel
from toolboxes.sysid import sysid

class Node_sysid(Node):
    """
    Saída desse método deve ser um dicionário em razão da grande quantidade de informações

    """
    def __init__(self, scene, title="Identificação de Sistemas", parent=None, method=None):
        super().__init__(Node=self)

        self.MODULO = 'Identificação de Sistemas'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = title
        self.method = method

        if method == 'Entrada e Saída':
            logging.info(NotImplementedError)
        elif method == 'O3KID':
            self.content = QDMNodeSysID(self)  # mando o node tambem
            self.grNode = QDMGraphicsID(self)
            self.grNode.resize(300, 200)
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)
            inputs = [0.2, 0.4]
            outputs = [{'pos': 0.7, 'type': 'dict'}]
            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()

class QDMGraphicsID(QDMGraphicsNode):
    def __init__(self, node, parent=None):
        super().__init__(node)

    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        super().paint(painter, QStyleOptionGraphicsItem, widget)
        # Adicionar funcionalidade extra ao No
        #svd_threshold = QPainterPath()
        #svd_threshold.addRect(0, 0, 100, 100)
        #painter.setPen(QPen(QColor('#ffa02f')))
        #painter.setBrush(QBrush(QColor('#ffffff')))
        #painter.drawPath(svd_threshold.simplified())


class QDMNodeSysID(QWidget):
    input_data = None
    output_data = None
    time_vector = None
    entrys  = []
    MODE = 'NOMODE'
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        svg_widget_time = SVGLabel()
        svg_widget_time.load(formula='\Delta t', fontsize=12, dpi=300, color='#a3a3a3', size=(30, 30))


        svg_widget = SVGLabel()
        svg_widget.load(formula='y_{k}', fontsize=12, dpi=300, color='#a3a3a3', size=(30, 30))



        self.layout.addWidget(svg_widget_time, 0, 0)
        self.layout.addWidget(svg_widget, 1, 0)


        ordem_LineEdit = QLineEdit()
        self.entrys.append(ordem_LineEdit)


        for entry in self.entrys:
            entry.textChanged.connect(self.node.updateNode)

        self.layout.addWidget(QLabel('Ordem'), 2, 0)
        self.layout.addWidget(ordem_LineEdit, 2, 1)

        dummy_file = 'data/Aquisicoes_03082020/1_Tratado.txt'
        with open(dummy_file) as file:
            self.data = np.loadtxt(file)                                    


    def refresh(self):
        t = self.data[:, 0]


        output_dict = {'Dados de treino': self.data[:, 1], 'Vetor tempo': t}
        self.node.sendSignal([output_dict],
                                        self.node.outputs,
                                        [self],
                                        ['dict'])

