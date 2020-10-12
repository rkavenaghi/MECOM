from PyQt5.QtGui import *
from PyQt5.Qt import *


class MiniMap(QWidget):
    # TODO fixar o mapa na tela. Como fazer isso?


    zoom_position = 1
    zoom_signal = pyqtSignal(float)

    minimap_xrange = 1
    minimap_xpos = 0

    minimap_yrange = 1
    minimap_ypos = 0

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.pen = QPen(QColor("#FF515151"))
        self.font = QFont("Ubuntu", 12)
        self.pen.setWidth(2)
        self.brush = QBrush(QColor("#FF313131"))

        # # Utilizado para que o minimapa nao seja reduzido ou aumentado durante o zoom
        # self.setFlag(QGraphicsItem.ItemIgnoresTransformations)
        # self.setFlag(QGraphicsObject.ItemSendsScenePositionChanges)
        # self.zoom_signal.connect(self.updateZoom)
        # self.setPos(self.mapToScene(750, 150))



    def updateMiniMapX(self):
        sent_signal = self.sender()
        if isinstance(sent_signal, QScrollBar):
            range = sent_signal.maximum() - sent_signal.minimum()
            if range != 0:
                self.minimap_xrange = sent_signal.pageStep()/(range)
                self.minimap_xpos = (1 - self.minimap_xrange)*(sent_signal.value() - sent_signal.minimum())/(range)
                self.update()
    def updateMiniMapY(self):
        sent_signal = self.sender()
        if isinstance(sent_signal, QScrollBar):
            range = sent_signal.maximum() - sent_signal.minimum()
            if range != 0:
                self.minimap_yrange = sent_signal.pageStep()/range
                self.minimap_ypos = (1 - self.minimap_yrange)*(sent_signal.value() - sent_signal.minimum())/(range)
                self.update()
    #
    # def boundingRect(self):
    #     return QRectF(0, 0, self.width+20, self.height)

    def minimapRect(self):
        #x0 = 10, y0 = 10
        return QRectF(10 + self.minimap_xpos*(self.width() -20),
                      10 + self.minimap_ypos*(self.height()-40),
                      self.minimap_xrange*(self.width() -20),
                      self.minimap_yrange*(self.height()-40))

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)

        outline = QPainterPath()
        outline.addRoundedRect(QRectF(0,0, self.width(), self.height()), 5, 5)
        painter.setRenderHints(QPainter.Antialiasing)
        painter.setPen(self.pen)
        painter.setBrush(self.brush)
        painter.drawPath(outline.simplified())

        self.minimap = QPainterPath()
        self.minimap.addRect(QRectF(10, 10, self.width() -20, self.height()-40))
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(QColor('#FF414141')))
        painter.drawPath(self.minimap)

        text = QPainterPath()
        text.addText(10, self.height()-10, self.font, f'Pos: {self.minimap_xpos:.3f}, {self.minimap_ypos:.3f}')
        painter.setPen(QPen(QColor('#ffffff')))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(text)

        minimap_dashed = QPainterPath()
        minimap_dashed.addRect(self.minimapRect())
        painter.setPen(QPen(QColor('#dada00')))
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(minimap_dashed)

        self.zoom_ellipse = QPainterPath()
        self.zoom_ellipse.addRoundedRect(QRectF(self.width() - 10, 0, 10, 200), 3, 2)

        pen_zoom = QPen(QColor('#ff00000'))
        pen_zoom.setWidth(1)
        painter.setPen(pen_zoom)
        painter.setBrush(QBrush(QColor('#a0a0a0aa')))
        painter.drawPath(self.zoom_ellipse)
        #
        zoom = QPainterPath()
        painter.setBrush(QBrush(QColor('ff0000')))
        painter.setPen(QPen(QColor('#ffffff')))
        zoom.addEllipse(self.width()-10, 200*(1-self.zoom_position) -5 , 9, 9)
        zoom.addText(self.width() ,  200*(1-self.zoom_position)+5 , self.font, f'{(1 - (200*(1-self.zoom_position))/200)*100:.0f}')
        painter.drawPath(zoom)

        text = QPainterPath()
        painter.setPen(QPen(QColor('#ffffff')))
        painter.setBrush(QBrush(QColor('#dadada')))
        painter.drawPath(text)

    def setScene(self, scene):
        self.scene = scene

    def updateZoom(self, value):
        print('Zoom event')
        self.zoom_position = value
        self.update()

        self.scene.zoomUpdate(self, value)

    def mousePressEvent(self, event):

        pos = event.pos() #Posicao do click em coordenadas do item
        if pos in self.minimap.boundingRect():
            #10 referente ao posicionamento do quadrado interno que representa o mapa
            x_coord, y_coord = pos.x() - 10, pos.y() - 10
            x_normalized = x_coord/(self.width - 20)
            y_normalized = y_coord/(self.height - 40)



            self.scene.views()[0].centerOn((x_normalized - 0.5)*self.scene.scene.scene_width,
                                           (y_normalized - 0.5)*self.scene.scene.scene_height)


        if pos in self.zoom_ellipse.boundingRect():
            self.zoom_event = event
            self.zoom_signal.emit(((-pos.y()+200)/200))

        super().mousePressEvent(event)