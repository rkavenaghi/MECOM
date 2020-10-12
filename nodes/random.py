from numpy import random, mean

from core.node import *
from core.node_edge import *

DEBUG = True


class Node_random(Node):
     def __init__(self, scene, title="Sem nome", parent=None, method=None):
        super().__init__(Node=self)
        self.MODULO = 'Random'
        self.MODULO_INITIALIZED = False 
        self.parent = parent
        self.scene = scene
        self.title = title
        
        self.content = QDMNodeRandom(self) #mando o node tambem
        self.grNode = QDMGraphicsNode(self)
        self.grNode.resize(240, 180)

        
        self.scene.addNode(self)
        self.scene.grScene.addItem(self.grNode)

        inputs = [0.27, 0.5, 0.65]
        outputs = [0.88]

        self.configInputsOutputs(inputs, outputs)

        self.inputs[0].setColor('refresh')
        self.inputs[1].setColor('int')
        self.inputs[2].setColor('float')
        self.outputs[0].setColor('float')

        self.configureObjectTree()

            
                
    

class QDMNodeRandom(QWidget):
    def __init__(self,node,parent=None):
        super().__init__()
        self.node = node
        self.initUI()
        
    def initUI(self):

        self.layout = QGridLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        refresh_label = QLabel('Refresh')
        label = QLabel('N')
        l2 = QLabel('Amplitude')
        
        e1 = QLineEdit() #tamanho do sinal 
        e2 = QLineEdit() #media do sinal
        
        
        e1.textEdited.connect(self.node.updateNode)
        e2.textEdited.connect(self.node.updateNode)
        
        self.entrys = [e1, e2]
        self.layout.addWidget(refresh_label, 0, 0)
        self.layout.addWidget(label, 1, 0)
        self.layout.addWidget(e1, 1, 1)
        
        
        self.layout.addWidget(l2, 2, 0)
        self.layout.addWidget(e2, 2, 1)

        self.layout.addWidget(QLabel('OUT1 : Vetor Random'), 3, 0)

        
    def result_calculation(self):

        entrySocket = [{'socket': self.node.inputs[1], 'entry': self.entrys[0]},
                       {'socket': self.node.inputs[2], 'entry': self.entrys[1]}]
        dados = self.node.checkConnectedEdgeData(entrySocket)
        if not '' in dados:

            e1, e2 = dados
            N = int(e1)
            p2 = float(e2)

            y = 2*p2*random.random(N)
            self.node.sendSignal([y - mean(y)], [self.node.outputs[0]], [self], ['float'])

    def refresh(self):
        self.result_calculation()
