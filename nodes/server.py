import numpy as np

from core.node import *
from core.node_socket import *
from utils.MECWidgets import SVGLabel
import logging

import socket
import threading

HEADER = 64
FORMAT = 'utf-8'

# Enviar Sinal para o Client



class Node_server(Node):

    def __init__(self, scene, title="Server", parent=None, method = None, data_type='float'):
        super().__init__(Node=self)
        self.data_type = data_type
        self.method = method
        self.scene = scene
        self.parent = parent
        self.MODULO_INITIALIZED = False

        self.title = 'Server'
        self.MODULO = 'Server'

        self.content = QDMNodeServer(self)
        self.grNode = QDMGraphicsNode(self)

        self.grNode.resize(300, 320)
        inputs = [0.8]
        outputs = []


        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        self.inputs = []
        self.outputs = []
        self.configInputsOutputs(inputs, outputs)
        self.configureObjectTree()

class QDMNodeServer(QWidget):

    clients = []

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)

        b1 = QPushButton('Start')
        b1.clicked.connect(self.serverConfiguration)
        b2 = QPushButton('Close')
        b2.clicked.connect(self.serverStop)
        l1 = QLabel('PORT')
        l2 = QLabel('SERVER')

        e1 = QLineEdit()
        e2 = QLineEdit()

        e1.setText('5050')
        e2.setText(socket.gethostbyname(socket.gethostname()))




        self.layout.addWidget(l1, 0, 0)
        self.layout.addWidget(e1, 0, 1)

        self.layout.addWidget(l2, 1, 0)
        self.layout.addWidget(e2, 1, 1)

        self.layout.addWidget(b1, 2, 0, 1, 1)
        self.layout.addWidget(b2, 2, 1, 1, 1)

        c = QComboBox()
        l3, e3 = QLabel('Comando'), QLineEdit()

        self.layout.addWidget(c, 3, 0, 1, 2)
        self.layout.addWidget(l3, 4, 0, 1, 1)
        self.layout.addWidget(e3, 4, 1, 1, 1)

        self.entrys = [e1, e2, e3]
        self.combobox = [c]

        b2 = QPushButton('Enviar')
        b2.clicked.connect(self.serverSendCommand)
        self.layout.addWidget(b2, 5, 0, 0, 1)

    def serverConfiguration(self):
        ADDRESS = (self.entrys[1].text(), int(self.entrys[0].text()))
        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind(ADDRESS)

        self.server_thread = threading.Thread(target=self.serverStart)
        self.server_thread._running = True
        self.server_thread.start()

    def serverStart(self):
        self.SERVER.listen()
        logging.info('Server Started')
        while self.server_thread._running:

            conn, address = self.SERVER.accept()
            thread = threading.Thread(target=self.handleClient, args=(conn, address))
            thread.start()
            logging.info(f"Conexão estabelecida. Número de conexões= {threading.active_count() - 2}")



    def serverStop(self):
        # TODO nao esta fechando adequadamente
        print('Fechar Server')

    def serverSendCommand(self):
        print('Enviar comando para o cliente')
        print(f'Comando = {self.entrys[2].text()}')
        index = self.combobox[0].currentIndex()
        self.clients[index]


    def handleClient(self, conn, address):
        logging.info(f'[{address}] [{conn}] ')
        client = (conn, address)
        if client not in self.clients:
            self.clients.append(client)
            self.combobox[0].addItem(f'{conn}')
        connected = True
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)

            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                logging.info(f'MENSAGEM ENVIADA = {msg}')

