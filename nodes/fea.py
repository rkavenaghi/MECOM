import OpenGL.GL as gl

from core.node import *
from core.node_socket import *

import logging
import stl
DEBUG = True


class Node_stl(Node):
    def __init__(self, scene, title="STL", parent=None, method=None):
        super().__init__(Node=self)
        self.MODULO = 'STL'
        self.MODULO_INITIALIZED = False
        self.scene = scene
        self.parent = parent
        self.title = title

        self.content = QDMNodeFEA(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(1000, 1000)
        self.grNode.initUI()

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [0.1, 0.2, 0.3,
                  {'pos': 0.4, 'type': 'string'},
                  {'pos': 0.55, 'type': 'float'},
                  {'pos': 0.6, 'type': 'float'},
                  {'pos': 0.65, 'type': 'float'}]

        outputs = [0.45]
        self.inputs = []
        self.outputs = []

        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()


class QDMNodeFEA(QWidget):

    objects = []
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)

        self.initUI()

    def initUI(self):
        self.glWidget = GLWidget()

        self.xSlider = self.createSlider()
        self.ySlider = self.createSlider()
        self.zSlider = self.createSlider()

        self.xSlider.valueChanged.connect(self.glWidget.setXRotation)
        self.glWidget.xRotationChanged.connect(self.xSlider.setValue)
        self.ySlider.valueChanged.connect(self.glWidget.setYRotation)
        self.glWidget.yRotationChanged.connect(self.ySlider.setValue)
        self.zSlider.valueChanged.connect(self.glWidget.setZRotation)
        self.glWidget.zRotationChanged.connect(self.zSlider.setValue)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.glWidget, 0, 0, 4, 4)
        mainLayout.addWidget(self.xSlider,  0, 5, 4, 1)
        mainLayout.addWidget(self.ySlider,  0, 6, 4, 1)
        mainLayout.addWidget(self.zSlider,  0, 7, 4, 1)


        lateral_frame = QFrame()
        lateral_layout = QVBoxLayout(lateral_frame)

        botao = QPushButton('Gerar um objeto ')
        botao.clicked.connect(self.createObjectInOpenGL)
        lateral_layout.addWidget(botao)

        move_x_entry = QLineEdit()
        move_x_entry.textChanged.connect(self.node.updateNode)
        move_y_entry = QLineEdit()
        move_y_entry.textChanged.connect(self.node.updateNode)
        move_z_entry = QLineEdit()
        move_z_entry.textChanged.connect(self.node.updateNode)

        self.entrys = [move_x_entry, move_y_entry, move_z_entry]
        lateral_layout.addWidget(move_x_entry)
        lateral_layout.addWidget(move_y_entry)
        lateral_layout.addWidget(move_z_entry)


        mainLayout.addWidget(lateral_frame, 0, 8, 1, 1)
        self.setLayout(mainLayout)
        self.xSlider.setValue(0)
        self.ySlider.setValue(0)
        self.zSlider.setValue(0)

    def createObjectInOpenGL(self):
        prosseguir = False

        try:
            object_mesh = stl.mesh.Mesh.from_file(self.node.inputs[3].edge.data)
            #self.objects.append(object_mesh) if object_mesh not in self.objects else None
            prosseguir = True
        except AttributeError:
            logging.error('Nao ha dados conectados ao Socket')
        except FileNotFoundError:
            logging.error('Arquivo não encontrado')

            

        if prosseguir:
            wireframe = True
            genList = gl.glGenLists(1)
            gl.glNewList(genList, gl.GL_COMPILE)
            for triangles,normal in zip(object_mesh.vectors, object_mesh.normals):
                gl.glColor3f(.100, .240, .410)
                node_0, node_1, node_2 = triangles[0:3]

                gl.glBegin(gl.GL_TRIANGLES)
                gl.glNormal3f(*normal)
                gl.glVertex3f(*node_0)
                gl.glVertex3f(*node_1)
                gl.glVertex3f(*node_2)
                gl.glEnd()

                gl.glBegin(gl.GL_LINE_LOOP)
                gl.glColor3f(0, 0, .300)
                gl.glVertex3f(*node_0)
                gl.glVertex3f(*node_1)
                gl.glVertex3f(*node_2)
                gl.glEnd()

            gl.glEndList()
            self.glWidget.object = genList


    def createSlider(self):
        slider = QSlider(Qt.Vertical)

        slider.setRange(0, 360)
        slider.setSingleStep(0.001)
        slider.setPageStep(1)
        slider.setTickInterval(20)
        slider.setTickPosition(QSlider.TicksRight)
        return slider

    def refresh(self):
        if self.node.inputs[0].hasSignal():
            dado = int(self.node.inputs[0].edge.data)
            self.xSlider.setValue(dado)
        if self.node.inputs[1].hasSignal():
            dado = int(self.node.inputs[1].edge.data)
            self.ySlider.setValue(dado)
        if self.node.inputs[2].hasSignal():
            dado = float(self.node.inputs[2].edge.data)
            self.glWidget.zRot = self.glWidget.normalizeAngle(dado)

        entry_data = [{'socket': self.node.inputs[4], 'entry':self.entrys[0]},
                      {'socket': self.node.inputs[5], 'entry':self.entrys[1]},
                      {'socket': self.node.inputs[6], 'entry':self.entrys[2]}]
        inputs_data = self.node.checkConnectedEdgeData(entry_data)

        try:
            x_translated = float(inputs_data[0])
            y_translated = float(inputs_data[1])
            z_translated = float(inputs_data[2])

            self.glWidget.translateX(x_translated)
            self.glWidget.translateY(y_translated)
            self.glWidget.translateZ(z_translated)

        except ValueError:
            logging.error('Não foi possível converter a entrada para FLOAT')


class GLWidget(QOpenGLWidget):

    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)


    def __init__(self, parent=None):
        super().__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

        self.lastPos = QPoint()

        self.trolltechGreen = QColor.fromCmykF(0.40, 0.0, 1.0, 0.0)
        self.backgroundColor = QColor.fromRgb(200, 200, 200, 255)
        self.colorred = QColor.fromRgb(255, 0, 0, 255)
        self.colorgreen = QColor.fromRgb(0, 255, 0, 255)
        self.colorblue = QColor.fromRgb(0, 0, 255, 255)

    def getOpenglInfo(self):
        info = """
            Vendor: {0}
            Renderer: {1}
            OpenGL Version: {2}
            Shader Version: {3}
        """.format(
            gl.glGetString(gl.GL_VENDOR),
            gl.glGetString(gl.GL_RENDERER),
            gl.glGetString(gl.GL_VERSION),
            gl.glGetString(gl.GL_SHADING_LANGUAGE_VERSION)
        )

        return info


    def sizeHint(self):
        return QSize(800, 400)

    def setXRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()

    def setYRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()

    def setZRotation(self, angle):
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()

    def translateX(self, x_val):
        self.x_pos = x_val

    def translateY(self, y_val):
        self.y_pos = y_val

    def translateZ(self, z_val):
        self.z_pos = z_val

    def initializeGL(self):
        print(self.getOpenglInfo())
        self.x_pos = 0
        self.y_pos = 0
        self.z_pos = 0
        self.setClearColor(self.backgroundColor.darker())
        self.object = self.makeObject()
        gl.glShadeModel(gl.GL_SMOOTH)
        gl.glEnable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_CULL_FACE)

    def paintGL(self):
        gl.glClear(
            gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
        gl.glLoadIdentity()
        gl.glTranslatef(self.x_pos, self.y_pos, self.z_pos)
        gl.glRotated(self.xRot, 1.0, 0.0, 0.0)
        gl.glRotated(self.yRot, 0.0, 1.0, 0.0)
        gl.glRotated(self.zRot, 0.0, 0.0, 1.0)
        gl.glCallList(self.object)

    def resizeGL(self, width, height):
        side = min(width, height)
        if side < 0:
            return

        gl.glViewport((width - side) // 2, (height - side) // 2, side,
                           side)

        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        gl.glOrtho(-600, +600, -800, 800, -250.0, 250.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def mousePressEvent(self, event):
        self.lastPos = event.pos()

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()

        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)

        self.lastPos = event.pos()

    def makeObject(self):
        genList = gl.glGenLists(1)
        gl.glNewList(genList, gl.GL_COMPILE)
        gl.glBegin(gl.GL_LINE_STRIP)

        gl.glEnd()
        gl.glEndList()

        return genList

    def normalizeAngle(self, angle):
        while angle < 0:
            angle += 360
        while angle > 360:
            angle -= 360
        return angle

    def setClearColor(self, c):
        gl.glClearColor(c.redF(), c.greenF(), c.blueF(), c.alphaF())

    def setColor(self, c):
        gl.glColor4f(c.redF(), c.greenF(), c.blueF(), c.alphaF())