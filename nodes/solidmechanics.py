from core.node import *
from core.cadeditor import *
import logging

class Node_solidmechanics(Node):

    def __init__(self, scene, title="Mecânica dos Sólidos", parent=None, method=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.MODULO = 'Vetor'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent

        self.method = method
        self.title = title



        if method == 'Desenhar seção':
            self.content = QDMNodeSectionDraw(self)
            self.grNode = QDMGraphicsNode(self)

            self.grNode.resize(400, 550)
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            self.configInputsOutputs()
            self.configureObjectTree()
        else:
            self.content = QDMNodeSolid(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(280, 450)
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            self.configInputsOutputs()
            self.configureObjectTree()

class QDMNodeSectionDraw(QWidget):

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.canvas = CanvasSection(self)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)

        vframe = QFrame()
        vlayout =QGridLayout(vframe)

        select_button = QPushButton('Select')
        line_draw = QPushButton('Linha')
        circle_draw = QPushButton('Círculo')
        poly_line_draw = QPushButton('Polilinha')
        ponto_draw = QPushButton('Ponto')
        self.botoes = [select_button, line_draw, circle_draw, poly_line_draw, ponto_draw]
        for botao in self.botoes:
            botao.clicked.connect(self.canvas.method)

        vlayout.addWidget(select_button, 0, 0)
        vlayout.addWidget(line_draw, 0, 1)
        vlayout.addWidget(circle_draw, 0, 2)
        vlayout.addWidget(ponto_draw, 1, 0)
        vlayout.addWidget(poly_line_draw, 1, 1)

        vframe.setFixedHeight(100)
        self.layout.addWidget(vframe, 0, 0)
        bg_widget = QFrame()
        bg_widget.setFixedHeight(300)
        bg_layout = QGridLayout(bg_widget)
        bg_layout.addWidget(self.canvas, 0, 0)
        self.layout.addWidget(bg_widget)
        self.entrys = [QLineEdit()]

        self.label = QLabel(' ')

        self.layout.addWidget(self.label)

        hframe = QFrame()
        hlayout = QHBoxLayout(hframe)

        hlayout.addWidget(self.entrys[0])
        sendcommand_b = QPushButton('Enter')
        sendcommand_b.setShortcut(Qt.Key_Enter)
        sendcommand_b.clicked.connect(self.sendEntryText)

        sendcommand_b.setFixedWidth(50)
        hlayout.addWidget(sendcommand_b)

        self.layout.addWidget(hframe)

    def sendEntryText(self):
        sentString = self.entrys[0].text()
        try:
            pos = [float(value) for value in sentString.split(',')]
            point = Ponto(*pos)
            # Aqui a transformacao tem que ser feita

            self.canvas.pontos.append(point)

        except TypeError as error:
            logging.error('Verifique a quantidade de argumentos')
            print(error)
        except ValueError as error:
            logging.warning('Tente novamente inserir a posição')
        except Exception as error:
            print(error)
            raise error

class CanvasSection(QWidget):
    OLDPOS = None
    NEWPOS = None

    METHOD = None

    lines = []
    pontos = []

    def __init__(self, parent=None):
        self.parent = parent
        super().__init__(parent)

    def method(self):
        self.METHOD = self.sender().text()

        if (self.METHOD == 'Linha' or self.METHOD == 'Polilinha'):
            self.OLDPOS = None
            self.NEWPOS = None

        if self.METHOD == 'Linha':
            self.parent.label.setText('Digite a posição do ponto inicial: ')

        elif self.METHOD == 'Ponto':
            self.parent.label.setText('Digite as coordenadas do ponto. Ex.: 5, 4')
        elif self.METHOD == 'Select':
            print('Obter o objeto correspondente ao desenho')

        else:
            self.parent.label.setText('Não implementado ainda')

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        self.canvas = QPainterPath()
        self.canvas.addRect(0, 0, self.width(), self.height())
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor('#3f3f3f')))
        painter.drawPath(self.canvas)

        for line in self.lines:


            line_path = QPainterPath(QPointF(*self.transformCoordinatesFromCanvas(*line.p_start.pos())))
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            line_path.lineTo(QPointF(*self.transformCoordinatesFromCanvas(*line.p_end.pos())))
            painter.drawPath(line_path)

        for point in self.pontos:
            circ = QPainterPath()
            circ.addEllipse(*self.transformCoordinatesFromCanvas(point.x, point.y), 4, 4)
            painter.setBrush(QBrush(QColor('#ffff00')))
            painter.setPen(Qt.NoPen)
            painter.drawPath(circ)


    def transformCoordinates(self, x, y):
        return x-self.width()/2, -y + self.height()/2

    def transformCoordinatesFromCanvas(self, x, y):
        return self.transformCoordinates(x + self.width(), y)



    def mousePressEvent(self, event):

        if event.pos() in self.canvas.boundingRect():

            self.OLDPOS = self.NEWPOS if self.NEWPOS is not None else None
            self.NEWPOS = event.pos()



            if (not isinstance(self.OLDPOS,type(None)) and self.METHOD == 'Linha'):



                xi = Ponto(self.OLDPOS.x(), self.OLDPOS.y())
                xf = Ponto(self.NEWPOS.x(), self.NEWPOS.y())
                line_obj = Linha(xi, xf)
                self.lines.append(line_obj)
                self.update()
                self.OLDPOS = None
                self.NEWPOS = None

            if (self.METHOD=='Ponto'):
                x_transformed, y_transformed = self.transformCoordinates(self.NEWPOS.x(), self.NEWPOS.y())
                point = Ponto(x_transformed, y_transformed)
                self.pontos.append(point)
                self.update()

            if self.METHOD == 'Select':

                x_pos = event.pos().x()
                y_pos = event.pos().y()
                list = []
                for objects in self.pontos:
                    if objects.region(*self.transformCoordinates(x_pos, y_pos)):
                        list.append(objects)
                print(list)



        else:
            super().mousePressEvent(event)













































class QDMNodeSolid(QWidget):

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def modechange(self):

        item_signal = self.sender()
        while self.function_layout.takeAt(0):
            pass

        if item_signal.currentText() == 'Propriedades de Seção':
            self.node.kwargs.update({'MODE': 'SECTION_PROPERTIES'})
            self.section_properties()

    def section_properties(self):
        self.function_layout.addWidget(QLabel('Viga Seção Retangular'))
        self.entrys = [QLineEdit(), QLineEdit()]
        self.output_entry = [QLineEdit(), QLineEdit()]
        hframe = QFrame()
        hlayout = QHBoxLayout(hframe)
        hlayout.addWidget(QLabel('Altura'))
        hlayout.addWidget(self.entrys[0])

        self.function_layout.addWidget(hframe)

        hframe = QFrame()
        hlayout = QHBoxLayout(hframe)
        hlayout.addWidget(QLabel('Largura'))
        hlayout.addWidget(self.entrys[1])

        self.function_layout.addWidget(hframe)
        self.function_layout.addWidget(QLabel('Propriedades de Seção'))


        hframe = QFrame()
        hlayout = QHBoxLayout(hframe)
        hlayout.addWidget(QLabel('Área: '))
        self.output_entry[0].setReadOnly(True)
        hlayout.addWidget(self.output_entry[0])
        self.function_layout.addWidget(hframe)

        hframe = QFrame()
        hlayout = QHBoxLayout(hframe)
        hlayout.addWidget(QLabel('Inércia: '))
        self.output_entry[1].setReadOnly(True)
        hlayout.addWidget(self.output_entry[1])
        self.function_layout.addWidget(hframe)

        for entry in self.entrys[0:2]:
            entry.textChanged.connect(self.updateProperties)

    def updateProperties(self):
        try:
            h, b = float(self.entrys[0].text()), float(self.entrys[1].text())
            A = h*b
            I = b*h**3/12
            self.output_entry[0].setText(f'{A:.3e}')
            self.output_entry[1].setText(f'{I:.3e}')
        except Exception as error:
            logging.warning(error)
            return

    def initUI(self):
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        label_1 = QLabel('Escolha um método')


        self.layout.addWidget(label_1)


        self.function_frame = QFrame()
        self.function_frame.setFixedSize(200, 300)
        self.function_layout = QVBoxLayout()
        self.function_frame.setLayout(self.function_layout)

        self.combobox = QComboBox()
        self.combobox.currentIndexChanged.connect(self.modechange)
        self.combobox.addItem('Selecione o método')
        self.combobox.addItem('Propriedades de Seção')
        self.layout.addWidget(self.combobox)
        self.layout.addWidget(self.function_frame)



