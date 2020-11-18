from core.node_edge import *
from core.node_socket import *
from utils.MECWidgets import SVGLabel, LineEntryEdit
from core.updateLogic import graphUpdateLogic

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.Qt import *
import utils
import logging


class Node:
    """
    Classe base para a criação de todas os nós. 

    Todos os métodos comuns a todos os nós devem ser referenciados
    nessa classe.
    """
    def __init__(self, Node=None, method=None, *args, **kwargs):

        self.kwargs = kwargs
        self.args = args
        self.id = id(self)
        self.method = method
        logging.info(f'Nó {Node}')

    def getOpenSockets(self):
        openSockets = []
        for socket in self.inputs + self.outputs:
            if socket.status:
                openSockets.append(socket)
        return openSockets

    def configureObjectTree(self):
        # TODO adicionar referencia a qual scene se refere os itens
        if not self.MODULO_INITIALIZED: 
            # Se o modulo nao estiver na arvore, adiciona-lo
            module_str = self.naming_objects(self.MODULO)
            self.module_str = module_str
            item = QTreeWidgetItem(self.parent.object_tree_documentation_tree_widget)

            item.node = self
            self.MODULO_OBJ = item
            
            item.setText(0, module_str)
        else:
            item = self.MODULO_OBJ
            
        # Se item ja tiver subitens, deletar todos, assim poderei atualizar
        children = []
        for child in range(item.childCount()):
            children.append(item.child(child))
        for child in children:
            item.removeChild(child)
        
        # Funciona perfeitamente para criar os dados etc...

        count_inputs, count_outputs = 0, 0
        for counter, socket in enumerate(self.inputs + self.outputs):
            if socket.position == 'input':
                cont = count_inputs
                count_inputs += 1
            elif socket.position == 'output':
                cont = count_outputs
                count_outputs += 1
            subitem = QTreeWidgetItem(item)
            subitem.setText(0, f'{socket.position}{cont}')
            if socket.hasEdges():
                edgeitem = QTreeWidgetItem(subitem)
                edgeitem.setText(0, f'Sinal')

                
    def naming_objects(self,modulo_string, objectCount=0):
        
        objectCount += 1
        if modulo_string+str(objectCount) not in self.parent.object_names:
            self.parent.object_names.append(modulo_string+str(objectCount))
            self.MODULO_INITIALIZED = True
            return modulo_string+str(objectCount)    
        else:
            return self.naming_objects(modulo_string, objectCount=objectCount)
  
    def configInputsOutputs(self, inputs=[], outputs=[]):
        
        self.inputs = []
        self.outputs = []

        for counter, socketPosition in enumerate(inputs):

            if isinstance(socketPosition, dict):
                socket = Socket(self, 'input', index=socketPosition['pos'],
                                data_type=socketPosition['type'],
                                label=socketPosition['label'] if 'label' in socketPosition.keys() else '',
                                multiple_edges=socketPosition['multiple_edges'] if 'multiple_edges' in socketPosition.keys() else True)
                self.inputs.append(socket)
            elif isinstance(socketPosition, float):

                socket = Socket(self, 'input', index=socketPosition)
                self.inputs.append(socket)

        for counter, socketPosition in enumerate(outputs):
            if isinstance(socketPosition, dict):

                socket = Socket(self, 'output', index=socketPosition['pos'],
                                data_type=socketPosition['type'],
                                label=socketPosition['label'] if 'label' in socketPosition.keys() else '',
                                multiple_edges=socketPosition['multiple_edges'] if 'multiple_edges' in socketPosition.keys() else True)
                self.outputs.append(socket)
            elif isinstance(socketPosition, float):
                socket = Socket(self, 'output', index=socketPosition)
                self.outputs.append(socket)

    def getSocketPosition(self, index, position):

        if position == 'input':
            x = 0
        elif position =='output':
            x = self.grNode.width

        # TODO colocar o valor do input
        y = index*self.grNode.height
        return [x, y]

    def updateConnectedEdges(self):
        for socket in self.inputs + self.outputs:
            if socket.hasEdges():
                for edges in socket.edges:
                    edges.updatePositions()

    @graphUpdateLogic
    def updateNode(self, *args, **kwargs):
        pass

    def propagate(self):
        """
        Classe para propagar os sinais atulizados para os próximos nós.
        :return:
        """
        for outputs in self.outputs:
            if outputs.hasEdges():
                for edge in outputs.edges:
                    edge.updateNodes()

    def id(self):
        self.id = id(self)

    def refresh(self):

        self.content.refresh()
        #self.scene.history.sceneStateChange()

    @property
    def pos(self):
        return self.grNode.pos() 

    def setPos(self, x, y):
        self.grNode.setPos(x, y)

    def checkConnectedEdgeData(self, entrySocket):
        """
        :argument: entrySocket

        :return: data, len(data), len(entrySocket)

        >>> entrySocket = [{'socket':self.inputs[0], 'entry':self.entry[0]},
                             {'socket':self.inputs[1], 'entry':self.entry[2]}]
        >>> node.checkConnectedEdgeData(entrySocket)
        """
        data = []

        for cont, pair in enumerate(entrySocket):

            input_socket = pair['socket']
            entry = pair['entry']

            if input_socket.hasEdge():
                data.append(input_socket.edge.data)
                entry.setEnabled(False)

                try:
                    entry.setText(f'{input_socket.edge.data:.3f}')
                # TODO verificar qual o erro e substuir exception
                except Exception as error:
                    print(error)
                    entry.setText(input_socket.edge.data) #em caso de ser uma string ja

            else:
                entry.setEnabled(True)
                data.append(entry.text())

        return data

    def renameNode(self):
        # TODO implementar lógica para renomear aqui
        print('Renomear nó aqui')
        #self.grNode.title_item.setPlainText('Oi')

    def invalidSignal(self):
        for output in self.outputs:
            if output.hasEdge():
                for edge in output.edges:
                    edge.signal(None, self, data_type='invalid')


    def removeNode(self): #Tem que estar atribuido a uma cena
        # TODO deletar as edges deletadas dos outros itens
        root = self.MODULO_OBJ.treeWidget().invisibleRootItem()
        root.removeChild(self.MODULO_OBJ)

        self.scene.removeNode(self)


    def setSelected(self, bool = False):
        self.grNode.setSelected(bool)

    def highlightTreeWidget(self, bool=False):
        if hasattr(self, 'MODULO_OBJ'):
            self.MODULO_OBJ.setSelected(bool)


    def sendSignal(self, datas, sockets, senders, data_types):
        """
        Enviar dado para todas as edges de Socket
        :param data:
        :param Socket Object:
        :return:
        """
        try:
            for data, socket, sender, data_type in zip(datas, sockets, senders, data_types):
                if socket.hasEdge():
                    for edge in socket.edges:
                        edge.signal(data, sender, data_type)

        except Exception as error:
            logging.error(error)
            print(self)
            self.invalidSignal()


    def edgeCreateEvent(self):
        pass

    def edgeDeleteEvent(self, edge):
        print('Reconfigurar sockets')
        # TODO ao deletar uma edge, reabilitar a entry correspondente, se houver.
        pass


    def tips(self):
        logging.info('reimplementado nessa classe, fazer uma classe base como exemplo e depois ir')
        widget = QDialog(self.content)
        layout = QVBoxLayout(widget)
        text = QPlainTextEdit(self.__doc__)
        logging.info(self.__doc__)
        text.setReadOnly(True)
        layout.addWidget(text)
        widget.show()

class QDMGraphicsNode(QGraphicsItem):
    # Override in children class
    def resize(self, width, height):
        self.width = width
        self.height = height
        self.initUI()

    def __init__(self, node, parent=None):
        super().__init__(parent)

        self.node = node
        self.content = self.node.content
        
        self._title_color = Qt.white
        self._title_font = QFont("Ubuntu", 12)
        
        self.width = 400
        self.height = 400
        self.edge_size = 10
        self.title_height = 24
        
        self._pen_default = QPen(QColor("#7f000000"))
        self._pen_selected = QPen(QColor("#FFFFA600"))
        self._brush_title = QBrush(QColor("#FF313131"))
        self._brush_backgroud = QBrush(QColor("#FF212121"))


        self.initUI()
        self.wasMoved = False

    def initSockets(self):
        pass

    def initContent(self):

        self.grContent = QGraphicsProxyWidget(self)
        self.content.setGeometry(self.edge_size, self.title_height + self.edge_size,
                                 self.width - 2*self.edge_size, self.height - 2*self.edge_size - self.title_height)
        self.grContent.setWidget(self.content)

    def initUI(self):
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.initTitle()
        self.title = self.node.title

        self.initSockets()
        self.initContent()


    def boundingRect(self):
        return QRectF(
            0,
            0,
            self.width,
            self.height,
        ).normalized()

    def initTitle(self):
        self.title_item = QGraphicsTextItem(self)
        self.title_item.setDefaultTextColor(self._title_color)
        self.title_item.setFont(self._title_font)
        self.title_item.setPos(0, 0)
        self.title_item.setTextWidth(self.width)



    @property
    def title(self): return self._title

    @title.setter
    def title(self, value):
        self._title = value

        # Função para renomear o título do Nó
        self.title_item.setPlainText(self._title)


    def paint(self, painter, QStyleOptionGraphicsItem, widget= None):
        # TODO adicionar Etiquetas ao codigo
        #comments = QPainterPath()
        #comments.addRoundedRect(QRectF(0, self.height - self.edge_size,
        #                               1*self.width, 0.2*self.height + self.edge_size),
        #                        self.edge_size, self.edge_size)
        #painter.setPen(Qt.NoPen)
        #painter.setBrush(QBrush(QColor('#AAcfcfcf')))
        #painter.drawPath(comments)
        
        path_title = QPainterPath()
        path_title.setFillRule(Qt.WindingFill)
        path_title.addRoundedRect(0, 0, self.width, self.title_height, self.edge_size, self.edge_size)
        path_title.addRect(0, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        path_title.addRect(self.width - self.edge_size, self.title_height - self.edge_size, self.edge_size, self.edge_size)
        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_title)
        painter.drawPath(path_title.simplified())

        self.hint_node = QPainterPath()
        self.hint_node.addEllipse(self.width -4*self.edge_size, (self.title_height - 15) / 2, 15, 15)

        painter.setBrush(QBrush(QColor('#575A61')))
        painter.setPen(Qt.NoPen)
        painter.drawPath(self.hint_node.simplified())

        hint_text = QPainterPath()
        hint_text.addText(self.width -4*self.edge_size +5.5, (self.title_height) / 2 +4, self._title_font, 'i')
        painter.setBrush(QBrush(QColor('#000000')))
        painter.setPen(Qt.NoPen)
        painter.drawPath(hint_text.simplified())

        self.exit_button = QPainterPath()
        self.exit_button.addEllipse(self.width - 2 * self.edge_size, (self.title_height - 15) / 2, 15, 15)

        painter.setBrush(QBrush(QColor('#ff5555')))
        painter.setPen(Qt.NoPen)
        painter.drawPath(self.exit_button.simplified())

        exit_text = QPainterPath()
        exit_text.addText(self.width -2*self.edge_size +4, (self.title_height) / 2 +3, self._title_font, 'x')
        painter.setBrush(QBrush(QColor('#000000')))
        painter.setPen(Qt.NoPen)
        painter.drawPath(exit_text.simplified())


        path_content = QPainterPath()
        path_content.setFillRule(Qt.WindingFill)
        path_content.addRoundedRect(0, self.title_height,
                                    self.width,
                                    self.height - self.title_height,
                                    self.edge_size, self.edge_size)

        path_content.addRect(0, self.title_height, self.edge_size, self.edge_size)
        path_content.addRect(self.width - self.edge_size, self.title_height, self.edge_size, self.edge_size)

        painter.setPen(Qt.NoPen)
        painter.setBrush(self._brush_backgroud)
        painter.drawPath(path_content.simplified())

        path_outline = QPainterPath()
        path_outline.addRoundedRect(0, 0, self.width, self.height, self.edge_size, self.edge_size)
        if self.isSelected():
            self.node.highlightTreeWidget(True)
        else:
            self.node.highlightTreeWidget(False)
        painter.setPen(self._pen_default if not self.isSelected() else self._pen_selected)
        painter.setBrush(Qt.NoBrush)
        painter.drawPath(path_outline.simplified())

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        for node in self.scene().scene.nodes:
            if node.grNode.isSelected():
                node.updateConnectedEdges()
        self.wasMoved = True

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        if self.wasMoved:
            self.wasMoved = False
            #if hasattr(self.node, 'module_str'):
            #    self.node.scene.history.sceneStateChange()

    def mousePressEvent(self, event):
        print('Evento em Node')
        if event.button() == Qt.LeftButton:
            position = event.pos()
            x_rel = position.x()/self.width
            y_rel = position.y()/self.height

            rectangle = self.hint_node.boundingRect()
            rectangle_close = self.exit_button.boundingRect()

            if position in rectangle:
                print('cliquei em hint, abrir tela com dicas de como usar a funcao')
                self.node.tips()
                return

            if position in rectangle_close:
                logging.info('Deletar Nó')
                self.node.removeNode()
                return

            # TODO avaliar a logica adequamento. Há algum evento capturando o sinal antes desse.
            if position in self.title_item.boundingRect():
                logging.info('Renomear Nó:: Abrir diálogo ')
                self.node.renameNode()


            logging.info(f'Cliquei em x_rel={x_rel} y_rel={y_rel}')
        else:
            super().mousePressEvent(event)

