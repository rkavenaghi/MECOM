from core.node import *
import numpy as np
import PyQt5.QtGui as QtGui
from toolboxes.mecanismos import loopclosure, quatrobarras
from utils.MECWidgets import SVGLabel

DEBUG = True
import logging

NOMETHOD = 0
LINE_DRAW = 1
SPLINE_DRAW = 2
ANCHOR = 3
POLILINHA = 4
ROTATE = 5

class Point2D():
    def __init__(self, x, y):
        """
        float x: Posicao em X
        float y: Posicao em Y
        """
        self.x = x
        self.y = y

    def coordinate(self):
        return (self.x, self.y)

class Line2D():
    def __init__(self, point_obj, point_obj2):
        self.start = point_obj
        self.end = point_obj2
        self.calc_length()

    def calc_length(self):
        self.length = ((self.start.x - self.end.x)**2 + (self.start.y - self.end.y)**2)**0.5


class Node_mecanismos(Node):
    def __init__(self, scene, title="Mecanismos 2D", parent=None, method=None):
        super().__init__()
        self.MODULO = 'Mecanismos 2D'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = title
        self.method = method
        self.content = QDMNodeMecanismos(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(800, 640)
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        if self.method == '4 Barras':
            logging.info('Análise de mecanismos 4 barras')

            inputs = [0.1, 0.2, 0.3, 0.4, 0.5]
            outputs = [{'pos': 0.7, 'type': 'float'}, {'pos': 0.8, 'type': 'complex'}]


            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()

class Canvas_Mecanismos(QWidget):

    linhas = []

    OLDPOS = None
    NEWPOS = None

    def __init__(self, node, parent=None):
        self.node = node
        self.font = QFont("Ubuntu", 12)
        super().__init__(parent)

    def paintEvent(self, event):
        super().paintEvent(event)

        painter = QPainter(self)
        self.canvas = QPainterPath()
        self.canvas.addRect(0, 0, self.width(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor('#3f3f3f')))
        painter.drawPath(self.canvas)

        linha = QPainterPath(QPointF(5, self.height()-5))
        linha.lineTo(QPointF(5, self.height()-25))
        linha.addText(5, self.height()-30, self.font, 'Y')
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor('#ffffff')))
        painter.drawPath(linha)

        linha = QPainterPath(QPointF(5, self.height()-5))
        linha.lineTo(QPointF(25, self.height()-5))
        linha.addText(30, self.height()-5, self.font, 'X')
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor('#ffffff')))
        painter.drawPath(linha)

        for lines in self.linhas:
            linha = QPainterPath(QPointF(*lines.start.coordinate()))
            linha.lineTo(QPointF(*lines.end.coordinate()))
            painter.setBrush(Qt.NoBrush)
            painter.setPen(QPen(QColor('#ffffff')))
            painter.drawPath(linha)

        super().paintEvent(event)

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Escape and
            not isinstance(self.node.content.CURRENT_METHOD, type(None))):
            self.node.content.CURRENT_METHOD = None
        else:
            super().keyPressEvent(event)



    def mousePressEvent(self, event):
        pos = event.pos()

        self.OLDPOS = self.NEWPOS if self.NEWPOS is not None else None
        self.NEWPOS = event.pos()

        if (self.node.content.CURRENT_METHOD == LINE_DRAW and
            not isinstance(self.OLDPOS, type(None))):

            self.linhas.append(Line2D(Point2D(self.OLDPOS.x(), self.OLDPOS.y()),
                                Point2D(self.NEWPOS.x(), self.NEWPOS.y())))
            self.OLDPOS = None
            self.NEWPOS = None
            self.node.content.CURRENT_METHOD = None
            self.update()
        if (self.node.content.CURRENT_METHOD == POLILINHA and
            not isinstance(self.OLDPOS, type(None))):

            self.linhas.append(Line2D(Point2D(self.OLDPOS.x(), self.OLDPOS.y()),
                                      Point2D(self.NEWPOS.x(), self.NEWPOS.y())))
            self.update()

    def screenCoordinateTransform(self):
        #Desenvolver as mudancas de coordenadas aqui
        pass


class QDMNodeMecanismos(QWidget):
    CURRENT_METHOD = None

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()



    def initUI(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)


        #adicionar_botoes em uma matrix de 2x10
        buttons = []
        for row in range(2):
            for col in range(10):
                b = QPushButton('')
                b.setFixedSize(50, 50)
                b.setIconSize(QSize(40, 40))
                b.METHOD = NOMETHOD
                b.METHODTEXT = "Nao implementado"

                self.layout.addWidget(b, row, col)
                buttons.append(b)
                b.clicked.connect(self.selectMethod)


        buttons[0].setIcon(QtGui.QIcon("resources/icons/mecanismos_line_icon.svg"))
        buttons[0].METHOD = LINE_DRAW
        buttons[0].METHODTEXT = "Elo"
        buttons[1].setIcon(QtGui.QIcon("resources/icons/mecanismos_spline_icon.svg"))
        buttons[1].METHOD = SPLINE_DRAW
        buttons[1].METHODTEXT = "Spline"
        buttons[2].setIcon(QtGui.QIcon("resources/icons/mecanismos_anchor_icon.svg"))
        buttons[2].METHOD = ANCHOR
        buttons[2].METHODTEXT = "Junta"

        buttons[3].setIcon(QtGui.QIcon("resources/icons/mecanismos_poliline_icon.svg"))
        buttons[3].METHOD = POLILINHA
        buttons[3].METHODTEXT = "Polilinha"

        buttons[4].setIcon(QtGui.QIcon("resources/icons/mecanismos_rotate_icon.svg"))
        buttons[4].METHOD = ROTATE
        buttons[4].METHODTEXT = "Atuador rotativo"

        self.layout.addWidget(frame)
        self.canvas = Canvas_Mecanismos(self.node)
        self.canvas.resize(600, 480)
        self.layout.addWidget(self.canvas, 2, 0, 1, 10)
        self.tip = QLabel(f'Método: {self.CURRENT_METHOD}')
        self.tip.setFixedHeight(40)
        self.layout.addWidget(self.tip, 3, 0, 1, 5)
        self.mouseCoordinate = QLabel('Pos:')
        self.layout.addWidget(self.mouseCoordinate, 3, 6, 1, 4)



    def mouseMoveEvent(self, event):
        x, y = event.pos().x(), event.pos().y()
        self.mouseCoordinate.setText(f'Pos: {x}, {y}')
        #print(self.canvas.geometry())
        #print(event.pos())
        #print(event.pos() in self.canvas.geometry())
        #self.node.content.mouseCoordinate.setText(f'Pos: {event.pos()}')
        super().mouseMoveEvent(event)

    def selectMethod(self):
        botao = self.sender()
        self.tip.setText(f'Método escolhido: {botao.METHODTEXT}')
        if botao.METHOD == LINE_DRAW:
            self.CURRENT_METHOD = LINE_DRAW
        if botao.METHOD == POLILINHA:
            self.CURRENT_METHOD = POLILINHA
        else:
            self.CURRENT_METHOD = NOMETHOD

    def refresh(self):

        entrySocket = [{'socket': self.node.inputs[0], 'entry': self.entrys[0]},
                       {'socket': self.node.inputs[1], 'entry': self.entrys[1]},
                       {'socket': self.node.inputs[2], 'entry': self.entrys[2]},
                       {'socket': self.node.inputs[3], 'entry': self.entrys[3]}]
        try:
            dados = self.node.checkConnectedEdgeData(entrySocket)

            C1, C2, C3, C4 = dados
            C = [float(C1), float(C2), float(C3), float(C4)]

            Q1 = np.deg2rad(np.r_[0:360:360j])
            x0 = np.deg2rad([45, 90])
            w1 = 1.
            h = np.abs(Q1[0] - Q1[1]) / w1

            mec = loopclosure.Mechanism(quatrobarras.Four_bar, Q1, C, h)
            mec.kinematics_solve(x0)
            P = loopclosure.Point([C[3], C[2]], [0., mec.values[1]], h, 360)

            self.node.sendSignal([Q1, P[0]], self.node.outputs, [self, self], ['float', 'complex'])


        except Exception as error:

            print(error)
            logging.warning('Erro detectado')



