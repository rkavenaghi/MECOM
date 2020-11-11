import math
from nodes import Node_group
from PyQt5 import QtGui

from core.node_edge import *
from core import clipboard
from core.node import *
import logging
import numpy as np

from core.minimap import MiniMap
from core.historyStack import SceneHistory


MODE_NOOP = 1
MODE_EDGE_DRAG = 2
MODE_EDGE_CUT = 3

class Scene:
    def __init__(self, title='Sem Nome', parent=None):
        self.id = id(self)
        self.parent = parent

        self.title = title
        self.nodes = []
        self.edges = []
        self.scene_width = 64000
        self.scene_height = 64000
        self.initUI()
        self.history = SceneHistory(self)
        self.clipboard = clipboard.Clipboard(self)

    def initUI(self):
        self.grScene = QDMGraphicsScene(self)
        self.grScene.setGrScene(self.scene_width, self.scene_height)

    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, edge):
        self.edges.append(edge)

    def removeNode(self, node):
        if node in self.nodes:
            self.grScene.removeNode(node)
            self.nodes.remove(node)

    def removeEdge(self, edge):
        if edge in self.edges:
            self.edges.remove(edge)

    def getNodeFromId(self, node_id):
        for node in self.nodes:
            if node.id == node_id:
                return node

    def groupNode(self, nodes, input_sockets, output_sockets):


        # TODO criar um Nó cujo tamanho depende do numero de sockets abertos e fechados

        # Fazer a parte gráfica desse nó

        Node_group(self, nodes, input_sockets, output_sockets, parent=self.parent)

class QDMCutLine(QGraphicsItem):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line_points = []
        self._pen = QPen(Qt.white)
        self._pen.setWidth(2)
        self._pen.setDashPattern([3, 3])
        self.setZValue(2)

    def boundingRect(self):
        return QRectF(0,0,1,1)

    def paint(self, painter, QStyleOptionsGraphicsItem, widget=None):
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(Qt.NoBrush)
        painter.setPen(self._pen)
        poly = QPolygonF(self.line_points)
        painter.drawPolygon(poly)

class QDMGraphicsView(QGraphicsView):
    def __init__(self, grScene, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.grScene = grScene
        self.initUI()
        self.setScene(self.grScene)
        self.mode = MODE_NOOP

        self.zoomInFactor = 1.25
        self.zoomClamp = True
        self.zoom = 10
        self.zoomStep = 1
        self.zoomRange = [0, 10]

        self.cutline = QDMCutLine()
        self.grScene.addItem(self.cutline)


    def initUI(self):
        self.setRenderHints(
            QPainter.Antialiasing | QPainter.HighQualityAntialiasing | QPainter.TextAntialiasing | QPainter.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.FullViewportUpdate)
        #self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        #self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)


    def mousePressEvent(self, event):
        print('Evento em scene')

        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonPress(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonPress(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonPress(event)
        else:
            super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MiddleButton:
            self.middleMouseButtonRelease(event)
        elif event.button() == Qt.LeftButton:
            self.leftMouseButtonRelease(event)
        elif event.button() == Qt.RightButton:
            self.rightMouseButtonRelease(event)
        else:
            super().mouseReleaseEvent(event)


    def middleMouseButtonPress(self, event):
        releaseEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                   Qt.LeftButton, Qt.NoButton, event.modifiers())

        super().mouseReleaseEvent(releaseEvent)
        self.setDragMode(QGraphicsView.ScrollHandDrag)

        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() | Qt.LeftButton, event.modifiers())
        super().mousePressEvent(fakeEvent)

    def middleMouseButtonRelease(self, event):

        fakeEvent = QMouseEvent(event.type(), event.localPos(), event.screenPos(),
                                Qt.LeftButton, event.buttons() & ~Qt.LeftButton, event.modifiers())

        super().mouseReleaseEvent(fakeEvent)
        self.setDragMode(QGraphicsView.NoDrag)

    def getItemAtClick(self, event):
        pos = event.pos()
        obj = self.itemAt(pos)
        return obj

    def edgeDragStart(self, item):

        self.previousEdge = item.socket.edge
        self.last_start_socket = item.socket

        self.dragEdge = Edge(self.grScene.scene, item.socket, None, EDGE_TYPE_BEZIER)
        logging.info(f"Criando edge {self.dragEdge} de {item.socket} ")

    def edgeDragEnd(self, item):
        """ return True if skip the rest of the code """
        self.mode = MODE_NOOP

        if type(item) is QDMGraphicsSocket:
            if (item.socket != self.last_start_socket and item.socket.allowEdge()):
                self.dragEdge.start_socket = self.last_start_socket
                self.dragEdge.end_socket = item.socket
                self.dragEdge.start_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.end_socket.setConnectedEdge(self.dragEdge)
                self.dragEdge.updatePositions()

                self.dragEdge.start_socket.node.updateNode()
                return True



        self.dragEdge.remove()
        self.dragEdge = None
        if self.previousEdge is not None:
            self.previousEdge.start_socket.edge = self.previousEdge
        return False

    def mouseMoveEvent(self, event):

        if self.mode == MODE_EDGE_DRAG:
            pos = self.mapToScene(event.pos())
            self.dragEdge.grEdge.setDestination(pos.x() - 5, pos.y())
            self.dragEdge.grEdge.update()

        if self.mode == MODE_EDGE_CUT:
            pos = self.mapToScene(event.pos())
            self.cutline.line_points.append(pos)
            self.cutline.update()

        super().mouseMoveEvent(event)

    def leftMouseButtonRelease(self, event):

        item = self.getItemAtClick(event)

        if self.mode == MODE_EDGE_DRAG:
            if id(item) == id(self.last_item_clicked):
                print('Item clicado foi igual')
            else:
                print('Item clicado diferente')
                self.mode = MODE_NOOP

                if type(item) == QDMGraphicsSocket:  # Se o item clicado é um socket de input, atribuir à edge ao end socket
                    if item.socket.position == 'input':
                        res = self.edgeDragEnd(item)
                        if res:
                            item.socket.edge.start_socket.node.configureObjectTree()
                            item.socket.edge.end_socket.node.configureObjectTree()
                            return
                    else:
                        logging.error('Tentativa de Conectar Sinal à Saída do Nó. Procedimento Abortado')
                        self.dragEdge.remove()


        if self.mode == MODE_EDGE_CUT:
            self.cutIntersectingEdges()
            self.cutline.line_points = []
            self.cutline.update()

            QApplication.setOverrideCursor(Qt.ArrowCursor)
            self.mode = MODE_NOOP
            return
        super().mouseReleaseEvent(event)

    def cutIntersectingEdges(self):

        for ix in range(len(self.cutline.line_points) - 1):
            p1 = self.cutline.line_points[ix]
            p2 = self.cutline.line_points[ix + 1]

            for edge in self.grScene.scene.edges:
                if edge.grEdge.intersectsWith(p1, p2):
                    edge.remove()

    def leftMouseButtonPress(self, event):

        item = self.getItemAtClick(event)
        self.last_item_clicked = item
        self.item_selected = item
        pos = event.pos()
        logging.info(f'Cliquei em {pos} item: {item}')

        if isinstance(item, QDMGraphicsSocket):  # Cliquei em um socket, comecar a desenhar a edge
            if item.socket.status:
                if self.mode == MODE_NOOP:
                    self.mode = MODE_EDGE_DRAG
                    self.edgeDragStart(item)

                elif self.mode == MODE_EDGE_DRAG:
                    res = self.edgeDragEnd(item)
                    if res: return

        if isinstance(item, type(None)):
            if event.modifiers() & Qt.ControlModifier:
                self.mode = MODE_EDGE_CUT
                fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
                                        Qt.LeftButton, Qt.NoButton, event.modifiers())
                super().mouseReleaseEvent(fakeEvent)
                QApplication.setOverrideCursor(Qt.CrossCursor)
                return
        super().mousePressEvent(event)


    def rightMouseButtonRelease(self, event):
        super().mouseReleaseEvent(event)

    def rightMouseButtonPress(self, event):
        item = self.getItemAtClick(event)
        if isinstance(item, QDMGraphicsSocket):
            logging.info(f'Socket status: {item.socket.status}')
            item.socket.changeStatus()


    def wheelEvent(self, event):
        zoomOutFactor = 1 / self.zoomInFactor
        if event.angleDelta().y() > 0:
            zoomFactor = self.zoomInFactor
            self.zoom += self.zoomStep
        else:
            zoomFactor = zoomOutFactor
            self.zoom -= self.zoomStep

        clamped = False
        if self.zoom < self.zoomRange[0]: self.zoom, clamped = self.zoomRange[0], True
        if self.zoom > self.zoomRange[1]: self.zoom, clamped = self.zoomRange[1], True

        if not clamped or self.zoomClamp is False:
            self.scale(zoomFactor, zoomFactor)
        #self.grScene.updateMapZoomCursor()

    def keyPressEvent(self, event):
        super().keyPressEvent(event)
        if event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and not event.modifiers() & Qt.ShiftModifier:
            self.grScene.scene.history.undo()

        elif event.key() == Qt.Key_Z and event.modifiers() & Qt.ControlModifier and event.modifiers() & Qt.ShiftModifier:
            self.grScene.scene.history.redo()

        elif event.key() == Qt.Key_C and event.modifiers() & Qt.ControlModifier:
            cursor_pos = QtGui.QCursor().pos()
            selected_nodes = []
            selected_edges = []
            for node in self.grScene.scene.nodes:
                if node.grNode.isSelected():
                    selected_nodes.append(node)
            for edge in self.grScene.scene.edges:
                if edge.grEdge.isSelected():
                    selected_edges.append(edge)
            logging.info(f"Nós {selected_nodes} e Edges {selected_edges} copiados para ClipBoard")
            self.grScene.scene.clipboard.content(selected_nodes+selected_edges, cursor_pos)
        elif event.key() == Qt.Key_V and event.modifiers() & Qt.ControlModifier:
            logging.info('Colar conteúdo da ClipBoard')
            self.grScene.scene.clipboard.paste(event)

        elif event.key() == Qt.Key_Delete:
            selected_nodes = []
            selected_edges = []
            for node in self.grScene.scene.nodes:
                if node.grNode.isSelected():
                    selected_nodes.append(node)

            for edge in self.grScene.scene.edges:
                if edge.grEdge.isSelected():
                    selected_edges.append(edge)

            for node in selected_nodes:
                node.removeNode()

            for edge in selected_edges:
                edge.remove()

        elif event.key() == Qt.Key_A and event.modifiers() & Qt.ControlModifier:
            for node in self.grScene.scene.nodes:
                node.setSelected(True)
            for edge in self.grScene.scene.edges:
                edge.grEdge.setSelected(True)





class NodeEditorWnd(QWidget):
    def __init__(self, mainwindow, title='Sem Nome', parent=None):
        super().__init__(parent)
        self.title = title
        self.mainwindow = mainwindow
        self.initUI()

    def initUI(self):
        self.setGeometry(200, 200, 800, 600)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)


        self.scene = Scene(title=self.title, parent=self.mainwindow)

        self.miniMap = self.mainwindow.MapDockWidget.minimap
        self.miniMap.setScene(self.scene.grScene)


        self.view = QDMGraphicsView(self.scene.grScene, self)
        self.view.horizontalScrollBar().setTracking(True)
        self.view.verticalScrollBar().setTracking(True)

        self.view.horizontalScrollBar().valueChanged.connect(self.mainwindow.MapDockWidget.minimap.updateMiniMapX)
        self.view.verticalScrollBar().valueChanged.connect(self.mainwindow.MapDockWidget.minimap.updateMiniMapY)
        self.layout.addWidget(self.view)
        self.show()



class QDMGraphicsScene(QGraphicsScene):
    def __init__(self, scene, parent=None): #scene = referencia a Scene
        super().__init__(parent)
        self.scene = scene
        self.gridSize = 20
        self.gridSquares = 5

        self._color_background = QColor("#393939")
        self._color_light = QColor("#2f2f2f")
        self._color_dark = QColor("#292929")

        self._pen_light = QPen(self._color_light)
        self._pen_light.setWidth(1)
        self._pen_dark = QPen(self._color_dark)
        self._pen_dark.setWidth(2)


        self.setBackgroundBrush(self._color_background)


    #
    # def updateMapZoomCursor(self):
    #     current_view = self.views()[0]
    #     self.minimap.zoom_position = current_view.zoom/(current_view.zoomRange[1]-current_view.zoomRange[0])
    #     self.minimap.update()

    def zoomUpdate(self, minimap, value):
        # Funcao utilizada pelo mapa para dar o zoom

        current_view = self.views()[0]
        print(current_view.zoom)
        #zoom_value = value*(current_view.zoomRange[1]-current_view.zoomRange[0])
        #if zoom_value > current_view.zoomRange[1]:
        #    zoom_value = current_view.zoomRange[1]
        #elif zoom_value< current_view.zoomRange[0]:
        #    zoom_value = current_view.zoomRange[0]
        #current_view.zoom = zoom_value



        #fakeWheelEvent = QWheelEvent(0, Qt.NoButton, event.modifiers())
        #QWheelEvent(pos, globalPos, pixelDelta, angleDelta, qt4Delta, qt4Orientation, buttons, modifiers)
        #fakeEvent = QMouseEvent(QEvent.MouseButtonRelease, event.localPos(), event.screenPos(),
        #                        Qt.LeftButton, Qt.NoButton, event.modifiers())
        #current_view.wheelEvent(fakeWheelEvent)

    def setGrScene(self, width, height):
        self.setSceneRect(-width // 2, -height // 2, width, height)

    def removeNode(self, node):
        try:
            for socket in node.inputs + node.outputs:
                if socket.hasEdge():
                    socket.edge.remove()
            if node in self.scene.nodes:
                self.removeItem(node.grNode)
        except AttributeError:
            logging.error('Não foi possível remover o Nó')

    def drawBackground(self, painter, rect):
        super().drawBackground(painter, rect)

        # here we create our grid
        left = int(math.floor(rect.left()))
        right = int(math.ceil(rect.right()))
        top = int(math.floor(rect.top()))
        bottom = int(math.ceil(rect.bottom()))

        first_left = left - (left % self.gridSize)
        first_top = top - (top % self.gridSize)

        # compute all lines to be drawn
        lines_light, lines_dark = [], []
        for x in range(first_left, right, self.gridSize):
            if (x % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(QLine(x, top, x, bottom))
            else:
                lines_dark.append(QLine(x, top, x, bottom))

        for y in range(first_top, bottom, self.gridSize):
            if (y % (self.gridSize * self.gridSquares) != 0):
                lines_light.append(QLine(left, y, right, y))
            else:
                lines_dark.append(QLine(left, y, right, y))

        painter.setPen(self._pen_light)
        painter.drawLines(*lines_light)
        painter.setPen(self._pen_dark)
        painter.drawLines(*lines_dark)

