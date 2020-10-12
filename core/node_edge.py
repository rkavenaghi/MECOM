from core.node_socket import *
from core.node import *
from configurations.appearence import Estilos
from core.edge_monitor import  updateMonitorWrapper, MonitorSinal



DEBUG = True

EDGE_TYPE_DIRECT = 1
EDGE_TYPE_BEZIER = 2

import logging




class Edge():

    DATATYPE_COLORS = Estilos().pallette
    data = None
    data_type = 'undefined'
    monitor = None


    def __init__(self, scene, start_socket, end_socket, edge_type=1):
        self.id = id(self)
        self.edge_type = edge_type
        self.scene = scene
        self.start_socket = start_socket
        self.end_socket = end_socket
        self.signal_valid = False

        self.start_socket.edge = self
        if self.end_socket is not None:
            self.end_socket.edge = self


        self.grEdge = QDMGraphicsEdgeDirect(self) if edge_type == EDGE_TYPE_DIRECT else QDMGraphicsEdgeBezier(self)
        self.updatePositions()

        self.scene.grScene.addItem(self.grEdge)
        self.scene.addEdge(self)

        #Create Edge Att Node


    def id(self):
        self.id = id(self)

    def signal(self, data, source, data_type='invalid'):
        """
        Classe base para configurar os sinais nas edges

         utilizada para:
         - diferenciar sinais de tipos de dados diferentes em cores distintas.

         data:=
         signal(data, source, data_type)

        """
        self.signal_source = source
        self.data = data
        self.data_type = data_type
        if self.data_type in self.DATATYPE_COLORS.keys():

            self.grEdge._pen = QPen(self.DATATYPE_COLORS[self.data_type])


    def updatePositions(self):

        source_pos = self.start_socket.getSocketPosition()
        source_pos[0] += self.start_socket.node.grNode.pos().x()
        source_pos[1] += self.start_socket.node.grNode.pos().y() 
        self.grEdge.setSource(*source_pos)
        if self.end_socket is not None:
            end_pos = self.end_socket.getSocketPosition()
            end_pos[0] += self.end_socket.node.grNode.pos().x() 
            end_pos[1] += self.end_socket.node.grNode.pos().y()
            self.grEdge.setDestination(*end_pos)
        else:
            self.grEdge.setDestination(*source_pos)

        self.grEdge.update()

    @updateMonitorWrapper
    def updateNodes(self, *args, **kwargs):
        """
        método para atualizar os nós conectados aos sockets de saída.
        :return:
        None
        """
        # obter os sockets e seus nos correspondentes. atualizar os nos de saida somente

        self.end_socket.node.updateNode()
            
    def remove_from_sockets(self):

        if self.start_socket is not None:
            try:
                self.start_socket.edges.remove(self)
            except ValueError:
                logging.error('Edge já foi removida')
            self.start_socket.node.configureObjectTree()
        if self.end_socket is not None:
            self.end_socket.edges.remove(self)
            self.end_socket.node.configureObjectTree()

        self.end_socket = None
        self.start_socket = None 

    def remove(self):
        start_socket = self.start_socket
        end_socket = self.end_socket

        self.remove_from_sockets()
        self.scene.grScene.removeItem(self.grEdge)
        self.scene.grScene.removeItem(self.monitor) if self.monitor != None else 0
        self.grEdge = None
        self.scene.removeEdge(self)


    def hasSignal(self):
        if isinstance(self.data, type(None)):
            return False
        else:
            return True


    
class QDMGraphicsEdge(QGraphicsPathItem):
    def __init__(self, edge, parent=None):
        super().__init__(parent)

        self.edge = edge


        self._color=QColor("#FFFFFF")
        self._color_selected = QColor('#00ff00')


        self._pen = QPen(self._color)
        self._pen_selected = QPen(self._color)
        self._pen_dragging = QPen(self._color)
        self._pen_dragging.setStyle(Qt.DashDotLine)

        self._pen.setWidthF(3)
        self._pen_selected.setWidthF(5)
        self._pen_dragging.setWidthF(2)

        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.zValue = -1

    def mousePressEvent(self, event):
        # Primeiro clique sobre a edge cria o monitor

        if self.edge.hasSignal():
            logging.info(f'Sinal de EDGE: {self.edge.data}')

        if event.button() == Qt.RightButton:
            click_pos = event.pos()
            monitor = MonitorSinal(self.edge.scene.grScene, self.edge)
            if isinstance(self.edge.monitor, type(None)):
                self.edge.scene.grScene.addItem(monitor)
                self.edge.monitor = monitor
                self.edge.monitor.setPos(self.mapToScene(click_pos))
                self.edge.monitor.moveBy(-50, -50)
            else:
                logging.info('Edge já tem monitor')
        super().mousePressEvent(event)
        
    def setSource(self, x, y):
        self.posSource = [x, y]

    def setDestination(self, x, y):
        self.posDestination = [x, y]

    def paint(self, painter, QStyleOptionGraphItem, widget=None):
        
        self.setPath(self.calcPath())
        if self.edge.end_socket == None:
            painter.setPen(self._pen_dragging)
        elif self.isSelected():
            painter.setPen(self._pen_selected)
        else:
            painter.setPen(self._pen)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(self.path())

    def calcPath(self):
        raise NotImplemented("This method has to be overriden in a child class")

    def intersectsWith(self, p1, p2):
        cutpath = QPainterPath(p1)
        cutpath.lineTo(p2)
        path = self.calcPath()
        return cutpath.intersects(path)

class QDMGraphicsEdgeDirect(QDMGraphicsEdge):

    def calcPath(self):
        path = QPainterPath(QPointF(self.posSource[0], self.posSource[1]))
        path.lineTo(self.posDestination[0], self.posDestination[1])
        return path

class QDMGraphicsEdgeBezier(QDMGraphicsEdge):

    def calcPath(self):
        s = self.posSource
        d = self.posDestination

        dist = (d[0] - s[0])*0.5
        if s[0] > d[0]:
            dist *= -1

        path = QPainterPath(QPointF(self.posSource[0],self.posSource[1]))
        path.cubicTo(s[0] + dist, s[1], d[0] - dist, d[1], self.posDestination[0], self.posDestination[1])
        return path




