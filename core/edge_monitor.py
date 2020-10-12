from PyQt5 import QtCore

from core.node_edge import *
from core.node_socket import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import logging

from numpy import ndarray, iscomplex
from functools import wraps


# Simplificar plot a medida que se afasta de view, ate omitir
def updateMonitorWrapper(function):
    @wraps(function)
    def wrapped(self, *args, **kwargs):
        # self é uma referência para Edge

        # Atualizar os dados do monitor aqui

        if not isinstance(self.monitor, type(None)):
            data = self.data if self.hasSignal() else None
            self.monitor.data = data

            self.monitor.REPAINT_LINES = True
            self.monitor.update()
        decoratedOutput = function(self, args, **kwargs)
        return decoratedOutput
    return wrapped

class MonitorSinal(QGraphicsObject):
    """
    Monitor é criado quando se clica com o botao direito no sinal.


    """
    height = 100
    width = 100
    monitor_width = width - 20
    monitor_height = height - 36
    REPAINT_LINES = True
    VALID = False
    data = None
    FLOAT = 0
    def __init__(self, scene, edge, parent=None):
        super().__init__(parent)
        self.scene = scene
        self.edge = edge
        self.parent = parent
        self.pen = QPen(QColor("#FF515151"))
        self.font = QFont("Ubuntu", 8)
        self.pen.setWidth(2)
        self.brush = QBrush(QColor("#FF313131"))
        self.data = self.edge.data
        self.setFlag(QGraphicsItem.ItemIsMovable)

    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    def normalizeData(self):
        if isinstance(self.data, float):
            self.FLOAT = 1
            self.float_value = self.data
            logging.info('Monitor não implementado para dados float')
            self.VALID = False

        elif isinstance(self.data, ndarray):
            try:
                self.data.shape[1]
                logging.info('Monitor não implementado para matrizes')
                self.VALID = False
            except IndexError:
                self._datalen = len(self.data)
                self._datarange = max(self.data) - min(self.data)
                self._databounds = [min(self.data), max(self.data)]
                self.VALID = True

    def paintData(self, index):
        x_normalized = 10 + index/(self._datalen - 1 )*self.monitor_width
        y_normalized = 18 + self.monitor_height*(1 - (self.data[index] - self._databounds[0])/(self._datarange))
        data_path = QPainterPath(QPointF(x_normalized, y_normalized))

        x_normalized_final = 10 + (index + 1) /(self._datalen - 1 ) * self.monitor_width
        y_normalized_final = 18 + self.monitor_height*(1 - (self.data[index + 1] - self._databounds[0])/(self._datarange))
        data_path.lineTo(QPointF(x_normalized_final, y_normalized_final))

        return data_path

    def mousePressEvent(self, event):
        if event.pos() in self.closeButtonRect():
            self.edge.scene.grScene.removeItem(self)
            self.edge.monitor = None
            return
        super().mousePressEvent(event)

    def closeButtonRect(self):

        return QRectF(self.width - 14, 4, 10, 10)

    def paint(self, painter, QStyleOptionsGraphicsItem, widget=None):

        monitor_outline = QPainterPath()
        monitor_outline.addRoundedRect(QRectF(0, 0, self.width, self.height), 5, 5)
        monitor_outline.addText(5, 10, self.font, 'Monitor')
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPath(monitor_outline)

        monitor_bg = QPainterPath()
        monitor_bg.addRect(QRectF(10, 18, self.monitor_width, self.monitor_height))
        painter.setPen(self.pen)
        painter.setBrush(QBrush(QColor('#FF515151')))
        painter.drawPath(monitor_bg)

        self._x_button = QPainterPath()
        self._x_button.addEllipse(self.width - 14, 4, 10, 10)

        painter.setPen(self.pen)
        painter.setBrush(QBrush(QColor('#ff0000')))
        painter.drawPath(self._x_button)

        if self.REPAINT_LINES:
            self.normalizeData()
            self.REPAINT_LINES = False

        if (self.VALID):
            painter.setPen(QPen(QColor('#dfdfdf')))
            painter.setBrush(Qt.NoBrush)
            for index in range(0, self._datalen-1):
                lines = self.paintData(index)
                painter.drawPath(lines)

        if (self.FLOAT):
            text = QPainterPath()
            painter.setPen(QPen(QColor('#ffffff')))
            painter.setBrush(Qt.NoBrush)
            text.addText(10, 50, self.font, f'Valor={self.float_value:.3e}')
            painter.drawPath(text)




