import glob
import sys
import serial

import time

from core.node import *


class Node_serial(Node):

    def __init__(self, scene, title="Bloco serial", parent=None, method=None):
        super().__init__(Node=self)

        self.MODULO = 'Porta Serial'
        self.MODULO_INITIALIZED = False
        self.method = method
        self.scene = scene
        self.parent = parent
        self.title = title

        self.content = QDMNodeSerial(self)
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(400, 530)

        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [0.14, 0.23, 0.33, 0.51]
        outputs = [0.63]
        self.configInputsOutputs(inputs, outputs)


        self.configureObjectTree()
        self.inputs[0].setColor('str')
        self.inputs[1].setColor('int')
        self.inputs[2].setColor('str')
        self.inputs[3].setColor('boolean')
        self.outputs[0].setColor('str')

    def updateNode(self):
        self.refresh()
        self.propagate()
        
        
        
    def refresh(self):

        # Enviar comando para a porta
        command = self.content.command_entry.text() if self.content.command_entry.text()!='' else None
        if not isinstance(command, type(None)):
            try:                                                
                self.content.ser.write(command.encode())
                data = self.content.readPortData()

                self.content.display_widget.setText(f'{data}')
                self.sendSignal([data.decode()], [self.outputs[0]], [self], ['str'])

            except AttributeError as error:
                logging.warning('Porta Serial nao foi aberta')

            else:
                print('Outro erro')

class QDMNodeSerial(QWidget):
    PORT_OPEN = False
    port = None
    baudrate = 9600
    timeout = 0
    #QUEUE = queue.Queue()
    #THREAD_LIST = list()
    
    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        list_port_botao = QPushButton('?')
        l1 = QLabel('Porta')
        l2 = QLabel('Baudrate')
        l3 = QLabel('Timeout')

        
        e1 = QLineEdit()
        e2 = QLineEdit()
        e3 = QLineEdit()
        self.command_entry = QLineEdit()




        list_port_botao.setMaximumSize(30, 30)

        hframe1 = QFrame()
        hlayout1 = QHBoxLayout(hframe1)
        hlayout1.addWidget(l1)
        hlayout1.addWidget(e1)
        hlayout1.addWidget(list_port_botao)

        hframe2 = QFrame()
        hlayout2 = QHBoxLayout(hframe2)
        hlayout2.addWidget(l2)
        hlayout2.addWidget(e2)

        hframe3 = QFrame()
        hlayout3 = QHBoxLayout(hframe3)
        hlayout3.addWidget(l3)
        hlayout3.addWidget(e3)



        setupFrame = QFrame()
        setupLayout = QVBoxLayout(setupFrame)
        setupLayout.addWidget(hframe1)
        setupLayout.addWidget(hframe2)
        setupLayout.addWidget(hframe3)

        setupFrame.setMaximumHeight(220)

        startSerial = QPushButton('Abrir Porta')
        endSerial = QPushButton('Fechar Porta')
        collectData = QPushButton('Enviar Comando')

        hframe4 = QFrame()
        hlayout4 = QHBoxLayout(hframe4)
        hlayout4.addWidget(collectData)
        hlayout4.addWidget(self.command_entry)

        startSerial.clicked.connect(self.startPort)
        endSerial.clicked.connect(self.closePort)
        collectData.clicked.connect(self.node.refresh)

        buttons_hframe = QFrame()
        buttons_hlayout = QHBoxLayout(buttons_hframe)

        buttons_hlayout.addWidget(startSerial)
        buttons_hlayout.addWidget(endSerial)


        self.layout.addWidget(setupFrame)

        self.displayFrame = QFrame()
        self.displayLayout = QVBoxLayout(self.displayFrame)
        self.displayLayout.addWidget(QLabel('Monitor Serial'))
        self.display_widget = QPlainTextEdit()
        
        self.display_widget.setFixedHeight(120)
        self.display_widget.setReadOnly(True)
        self.displayLayout.addWidget(self.display_widget)
        self.layout.addWidget(buttons_hframe)
        self.layout.addWidget(hframe4)
        self.layout.addWidget(self.displayFrame)

        list_port_botao.clicked.connect(self.serial_ports_load)
        
        self.entrys = [e1, e2, e3, self.command_entry]
        
    def configurePort(self):
        entrySocket = [{'socket': self.node.inputs[0], 'entry': self.entrys[0]},
                       {'socket': self.node.inputs[1], 'entry': self.entrys[1]},
                       {'socket': self.node.inputs[2], 'entry': self.entrys[2]}]
        
        dados = self.node.checkConnectedEdgeData(entrySocket)


        self.port = dados[0] if dados[0]!='' else self.port
        self.baudrate = int(dados[1]) if dados[1]!='' else self.baudrate
        self.timeout = float(dados[2]) if dados[2]!='' else self.timeout


    def portINFO(self):
        info =  f"""
                Porta {self.port} 
                Baudrate {self.baudrate}
                Timeout {self.timeout}
                """
        return info

    def startPort(self):

        try:
            self.configurePort()
            self.ser = serial.Serial(self.port, self.baudrate, timeout=self.timeout)

            time.sleep(1) #Tempo para abrir a porta
            self.ser.flushInput()
            self.PORT_OPEN = True
            
        except serial.SerialException:
            logging.error('Não foi possível abrir esta porta.')

    def readPortData(self):
        if self.PORT_OPEN:
            bytesToRead = self.ser.inWaiting()
            data = self.ser.read(bytesToRead)
            self.display_widget.setText(data.decode())
            return data

    def closePort(self):
        try:
            if self.ser.isOpen():
                self.ser.close()
                logging.info('Porta Encerrada')
                self.PORT_OPEN = False
        except:
            logging.error('Alguma coisa deu errado')



    def serial_ports_load(self):

        widget = QDialog(self)
        layout = QVBoxLayout(widget)
        layout.addWidget(QLabel('Portas disponiveis'))
        for ports in self.serial_ports():
            radiobutton = QRadioButton(ports)
            layout.addWidget(radiobutton)
            radiobutton.toggled.connect(self.selectedPort)


        close_button = QPushButton('Fechar')

        close_button.clicked.connect(widget.close)
        hframe = QFrame()
        h_layout = QHBoxLayout(hframe)

        h_layout.addWidget(close_button)
        layout.addWidget(hframe)
        widget.show()

    def selectedPort(self):
        if self.sender().isChecked():
            self.port = self.sender().text()
            self.entrys[0].setText(self.sender().text())
            self.sender().parent().close()

    def serial_ports(self):
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass

        return result




