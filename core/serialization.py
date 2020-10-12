from collections import OrderedDict
import json

from gui.tree_widget_configuration import *
from nodes import *
from core.node_edge import Edge


# TODO melhorar comandos para undo e redo
class Serialization:

    def __init__(self, Session=None, currentInstance=None, sender=None, filename=None):
        self.Session = Session

        # self.instance = NodeEditorWnd
        self.instance = currentInstance
        if isinstance(filename, type(None)):
            self.filename = 'examples/SCENE.txt'
        else:
            self.filename = filename

        print(self.filename)
        if not isinstance(sender, type(None)):

            if sender == 'Salvar':
                logging.info(f'Salvar Arquivo {self.filename}')

                self.instance = currentInstance
                print('Entrei em Serialization ')
                logging.info(f'Salver {currentInstance}')
                logging.info('Classe Serialization')
                self.serialize()

            elif sender == 'Abrir' or sender == 'Abrir Recente':
                logging.info(f'Abrir Arquivo {self.filename}')

                with open(self.filename, "r") as file:
                    raw_data = file.read()
                    data = json.loads(raw_data, encoding='utf-8')
                    logging.info(f'Arquivo {self.filename} carregado com sucesso')
                self.deserialize(data)

            elif sender == 'Salvar como':
                logging.info(f'Salvando Scene em {filename}')
                self.serialize()


    def serialize(self):
        self.sceneSerialization(self.instance.scene)

    def lembreteCheckBoxSerialization(self, checkbox):
        return OrderedDict([('state', checkbox.isChecked())])

    def lembreteSerialization(self, lembrete):
        checkboxes = []
        for checkbox in lembrete.checkboxes:
            checkboxes.append(self.lembreteCheckBoxSerialization(checkbox))

        return OrderedDict([('texto', lembrete.plaintextedit.toPlainText()),
                            ('checkbox', checkboxes),
                            ('width', lembrete.width()),
                            ('height', lembrete.height()),
                            ('x', lembrete.pos().x()),
                            ('y', lembrete.pos().y())])

    def sceneSerialization(self, scene, only_scene=0):


        nodes, edges, lembretes = [], [], []

        for node in scene.nodes:
            nodes.append(self.nodeSerialization(node))

        for edge in scene.edges:
            edges.append(self.edgeSerialization(edge))

        if not isinstance(self.Session, type(None)):
            for lembrete in self.Session.lembretes: lembretes.append(self.lembreteSerialization(lembrete))

        retString = OrderedDict([('id', scene.id),
                                 ('scene', scene.title),
                                 ('width', scene.scene_width),
                                 ('height', scene.scene_height),
                                 ('nodes', nodes),
                                 ('edges', edges),
                                 ('lembretes', lembretes)
                                 ])
        if only_scene:
            return retString

        with open(self.filename, 'w') as file:
            file.write(json.dumps(retString, indent=4))
            logging.info(f'ARQUIVO {file} SALVO COM SUCESSO! ')

    def nodeSerialization(self, node):
        inputsockets = []
        outputsockets = []
        entrys = []
        checkboxes = []
        plainText = []
        for sockets in node.inputs:
            inputsockets.append(self.socketSerialization(sockets))
        for sockets in node.outputs:
            outputsockets.append(self.socketSerialization(sockets))
        if hasattr(node.content, 'entrys'):
            logging.info('Salvando dados dos nós fornecidos pelo usuário')
            for entry in node.content.entrys:
                entrys.append(self.entrySerialization(node, entry))
        if hasattr(node.content, 'checkboxes'):
            for checkbox in node.content.checkboxes:
                checkboxes.append(self.checkboxSerialization(node, checkbox))
        if hasattr(node.content, 'plainText'):
            for plaintext in node.content.plainText:
                plainText.append(self.plainTextSerialization(node, plaintext))

        return OrderedDict([('id', node.id),
                     ('class', type(node).__name__),
                     ('module', node.module_str),
                     ('x_pos', node.pos.x()),
                     ('y_pos', node.pos.y()),
                     ('title', node.title),
                     ('inputs', inputsockets),
                     ('outputs', outputsockets),
                     ('sender', node.method),
                     ('entrys', entrys),
                     ('kwargs', node.kwargs),
                     ('args', node.args),
                     ('checkboxes', checkboxes),
                     ('plainText', plainText),
                     ])

    def plainTextSerialization(self, node, plainText):
        return OrderedDict([('text', plainText.toPlainText())])

    def checkboxSerialization(self, node, checkbox):
        index = node.content.checkboxes.index(checkbox)
        status = checkbox.isChecked()
        return OrderedDict([('index', index),
                            ('status', status)])

    def entrySerialization(self, node, entry):
        index = node.content.entrys.index(entry)
        value = entry.text()
        return OrderedDict([('index', index),
                            ('valor', value)])

    def edgeSerialization(self, edge):
        return OrderedDict([('id', id(edge.id)),
                            ('StartSocket', id(edge.start_socket)),
                            ('EndSocket', id(edge.end_socket)),
                            ('edge_type', edge.edge_type)])
            
    def socketSerialization(self, socket):
        return OrderedDict([('id', id(socket)),
                            ('position', socket.position),
                            ('color', socket.socket_color),
                            ('status', socket.status)
                            ])

    def nodeDeserialize(self, data, scene=None, hashmap={}, same_id=True):

        node_class = globals()[data['class']]
        if isinstance(scene, type(None)):
            node_scene = self.Session.current_project.scene
            node_session = self.Session
        else:
            node_scene = scene
            node_session = scene.parent.mainwindow

        Node = node_class(node_scene,
                          parent=node_session,
                          method=data['sender'],
                          *data['args'],
                          **data['kwargs'])

        Node.setPos(data['x_pos'], data['y_pos'])
        if same_id:
            Node.id = data['id']

        for cont, inputs in enumerate(Node.inputs):
            inputs.id = data['inputs'][cont]['id']
            inputs.setStatus(data['inputs'][cont]['status'])
        for cont, outputs in enumerate(Node.outputs):
            outputs.id = data['outputs'][cont]['id']
            outputs.setStatus(data['outputs'][cont]['status'])
        logging.info('Carregando dados do Nó')
        try:
            for entrydata in data['entrys']:
                Node.content.entrys[entrydata['index']].setText(entrydata['valor'])
        except AttributeError:
            logging.error('Nao encontrada entrys, pular')

        for checkboxdata in data['checkboxes']:
            Node.content.checkboxes[checkboxdata['index']].setChecked(checkboxdata['status'])
        for index, plainText in enumerate(data['plainText']):
            Node.content.plainText[index].setText(plainText['text'])

        return Node

    def edgeDeserialize(self, edge, nodes, hashmap={}):
        logging.info('Carregar edge')

        start_socket_id = edge['StartSocket']
        end_socket_id = edge['EndSocket']
        
        logging.info(f'carregando edge de {start_socket_id} a {end_socket_id}')
        
        for node in nodes:

            for cont, socketinput in enumerate(node['inputs']):

                if (socketinput['id'] == end_socket_id):

                    startSocketNode = node
                    startSocket = cont

            for cont, socketoutput in enumerate(node['outputs']):
                if socketoutput['id'] == start_socket_id:
                    endSocketNode = node
                    endSocket = cont

        for node in self.Session.current_project.scene.nodes:
            if node.id == startSocketNode['id']:

                startNode = node
            elif node.id == endSocketNode['id']:

                endNode = node

        drawedge = Edge(self.Session.current_project.scene,
                        endNode.outputs[endSocket],
                        startNode.inputs[startSocket],
                        edge_type=edge['edge_type'])

        drawedge.start_socket = endNode.outputs[endSocket]
        drawedge.end_socket = startNode.inputs[startSocket]
        drawedge.start_socket.setConnectedEdge(drawedge)
        drawedge.end_socket.setConnectedEdge(drawedge)
        drawedge.updatePositions()
        drawedge.id = edge['id']

        logging.info('edge carregada')



    def sceneDeserialize(self, data, scene=None, hashmap={}):
        if not isinstance(scene, type(None)):
            for nodedata in data['nodes']:
                self.nodeDeserialize(nodedata, scene=scene)
            for edgedata in data['edges']:
                self.edgeDeserialize(edgedata, data['nodes'])
            return

        logging.info('Carregando projeto')
        titulo = data['scene']
        self.Session.new_project(title=titulo)
        self.Session.current_project.scene.id = data['id']
        for nodedata in data['nodes']:
            self.nodeDeserialize(nodedata)
        for edgedata in data['edges']:
            self.edgeDeserialize(edgedata, data['nodes'])
        self.lembreteDeserialize(data['lembretes'])

    def lembreteDeserialize(self, lembretes, hashmap={}):

        for cont, lembrete in enumerate(lembretes):

            texto = lembrete['texto']
            cb_states = [cb['state'] for cb in lembrete['checkbox']]
            self.Session.lembrete_function()

            self.Session.lembretes[cont].plaintextedit.setPlainText(texto)
            self.Session.lembretes[cont].resize(lembrete['width'], lembrete['height'])
            for cont2, cboxes in enumerate(self.Session.lembretes[cont].checkboxes):

                cboxes.setChecked(cb_states[cont2])


    def deserialize(self, data, hashmap={}):
        self.sceneDeserialize(data)






