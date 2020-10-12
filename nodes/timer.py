from core.node import *
from core.node_edge import *
from PyQt5.QtWidgets import (QLabel, QPushButton, QWidget, QGridLayout, QCheckBox, QLineEdit)

from PyQt5.QtCore import QTimer



class Node_timer(Node):
    def __init__(self,scene,title="Sem nome",parent=None, method=None):
        super().__init__(Node = self)
        self.MODULO = 'Timer'
        self.MODULO_INITIALIZED = False
        self.parent = parent 
        self.scene = scene
        
        self.title = title
        
        self.content = QDMNodeTimerContentWidget()
        self.content.parent = self
        
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(240, 280)
        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = []
        outputs = [0.7, 0.8]
        self.configInputsOutputs(inputs,outputs)
        self.configureObjectTree()

        self.outputs[0].setColor('float')
        self.outputs[1].setColor('refresh')




class QDMNodeTimerContentWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.initUI()


    def initUI(self):
        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
    

   
        l1 = QLabel('Valor inicial')
        l2 = QLabel('Valor final')
        l3 = QLabel('Passo')
        l4 = QLabel('Valor atual: ')

        self.current_instant_label = QLabel('')
        e1 = QLineEdit()
        e2 = QLineEdit()
        e3 = QLineEdit()
        e4 = QCheckBox('Loop')
        e4.setCheckable(True)
        e4.setChecked(True)
        e5 = QLineEdit()
        l5 = QLabel('Tempo atualizar')

        
        b1 = QPushButton('Iniciar')
        
        b1.clicked.connect(self.startTimer)
        self.pause_button = QPushButton('Pausar')
        self.pause_button.clicked.connect(self.botaoClicado)


        
        self.entrys = [e1,e2,e3,e4,e5]
        self.layout.addWidget(l1, 0, 0) #Valor inicial
        self.layout.addWidget(e1, 0, 1)

        self.layout.addWidget(l2, 1, 0) #Valor final
        self.layout.addWidget(e2, 1, 1)


        self.layout.addWidget(l3, 2, 0) #Passo
        self.layout.addWidget(e3, 2, 1)

        # Refresh time
        self.layout.addWidget(l5, 3, 0)
        self.layout.addWidget(e5, 3, 1)
        

        self.layout.addWidget(e4, 4, 0) #Loop
        self.layout.addWidget(l4, 5, 0) #Current instant tempo
        self.layout.addWidget(self.current_instant_label, 5, 1)
        self.layout.addWidget(QLabel('Refresh'))
        self.layout.addWidget(b1, 7, 0) #Comecar
        self.layout.addWidget(self.pause_button, 7, 1) #Parar

        self.setLayout(self.layout)

    def refresh(self):
        try:
            if self.node.outputs[0].hasEdges():
                for edge in self.node.outputs[0].edges:
                    edge.signal(self.timer_parameters['t_current'], self, 'float')
            if self.node.outputs[1].hasEdges():
                for edge in self.node.outputs[0].edges:
                    edge.end_socket.node.updateNode()
        except AttributeError:
            logging.error('Timer ainda não está completamente definido')


    def startTimer(self):
        if DEBUG: print('Temporizador iniciado')
        try:
            
            t0 = float(self.entrys[0].text())
            tf = float(self.entrys[1].text())
            tstep = float(self.entrys[2].text())
            
            t_interval = float(self.entrys[4].text())
            self.current_instant = t0 
            self.timer_parameters = {'t_init': t0,
                                     't_end': tf,
                                     't_step': tstep,
                                     't_current': self.current_instant}

            self.timer = QTimer()
            self.timer.setInterval(t_interval)
            self.timer.timeout.connect(self.updateTimer)
            self.pause_button.setText('Pausar')
            self.timer.start()


        # TODO modificar este comportamento. DESIGN RUIM DE PROGRAMA
        except:
            print('Temporizador nao configurado corretamente')

    def botaoClicado(self):
        item = self.sender()
        if item.text() == 'Pausar':

            self.timer.stop()
            self.pause_button.setText('Retomar')
        elif item.text() == 'Retomar':
            self.pause_button.setText('Pausar')
            self.timer.start()
            

    def updateTimer(self):

        if self.timer_parameters['t_current'] < self.timer_parameters['t_end']:
            self.timer_parameters['t_current'] += self.timer_parameters['t_step']
        elif not bool(self.entrys[3].isChecked()):
            # TODO testar essa linha
            self.timer.stop()
        else:
            self.timer_parameters['t_current'] = self.timer_parameters['t_init']

        self.parent.timer_parameters = self.timer_parameters
        self.current_instant_label.setText(f" {self.timer_parameters['t_current']:2f} ")
        self.parent.updateNode()
        
        



    
