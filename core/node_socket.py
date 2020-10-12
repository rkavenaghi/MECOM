from core.node_edge import *
from configurations.appearence import Estilos
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

LEFT_TOP = 1
LEFT_BOTTOM = 2
RIGHT_TOP = 3
RIGHT_BOTTOM = 4

import logging
class Socket:

    status = 0

    def __init__(self, node, position, index=0, data_type='float', label=' ', multiple_edges=True):
        self.id = id(self)
        self.node = node 
        self.index = index
        self.data_type = data_type
        self.socket_color = data_type

        self.position = position
        self.label = label
        self.multiple_edges = multiple_edges

        self.grSocket = QDMGraphicsSocket(self, socket_type=self.data_type)
        self.grSocket.setPos(*self.node.getSocketPosition(index, self.position))
        self.changeStatus()
        self.edge = None 
        self.edges = []
        
    def setConnectedEdge(self, edge=None):
        self.edge = edge
        self.edges.append(edge)

    def getSocketPosition(self):
        # TODO colocar aqui a posicao adequada
        return self.node.getSocketPosition(self.index, self.position)

    def allowEdge(self):
        if self.hasEdge() and self.multiple_edges:
            return True
        elif isinstance(self.edge, type(None)):
            return True
        else:
            logging.error('Socket não permite múltiplas entradas. Sinal removido')
            return False

    def hasEdge(self):
        return self.edge is not None

    def setStatus(self, boolean):
        self.status = boolean

        if boolean:
            self.enableSocket()
            self.grSocket._brush = QBrush(self.grSocket._colors[self.socket_color])
            self.grSocket.setFlag(QGraphicsItem.ItemIsSelectable, True)

        else:
            self.disableSocket()
            self.grSocket.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.grSocket.update()

    def changeStatus(self):
        self.status = not self.status
        self.setStatus(self.status)

    def enableSocket(self):
        self.grSocket.setOpacity(1)
    def disableSocket(self):
        self.grSocket.setOpacity(0.35)


    def hasSignal(self):

        if self.hasEdge():
            return self.edge.hasSignal()
        else:
            return False

    def hasEdges(self):
        return True if len(self.edges) != 0 else False

    def setColor(self, color_index=0):

        self.grSocket._brush = QBrush(self.grSocket._colors[color_index])


class QDMGraphicsSocket(QGraphicsItem):
    _colors = Estilos().default()



    def __init__(self, socket, socket_type):
        self.socket = socket
        super().__init__(socket.node.grNode)
        self.radius = 8
        self.outline_width = 2

        self._color_background = self._colors[socket_type]
        self._color_outline = QColor("#FF000000")
        self._color_selected = QColor("#afafaf")

        self._pen = QPen(self._color_outline)
        self._pen.setWidth(self.outline_width)
        self._brush = QBrush(self._color_background)
        self._pen_selected = QPen(self._color_selected)




    def paint(self, painter, QStyleOptionGraphicsItem, widget=None):
        #painting circle 
        painter.setBrush(self._brush)
        painter.setPen(self._pen) if not self.isSelected() else painter.setPen(self._pen_selected)
        painter.drawEllipse(-self.radius, -self.radius, 2*self.radius, 2*self.radius)

    def boundingRect(self):
        return QRectF(
            -self.radius -self.outline_width,
            -self.radius -self.outline_width,
            2*(self.radius + self.outline_width),
            2*(self.radius + self.outline_width)
        )
