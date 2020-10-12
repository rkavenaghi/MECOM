import numpy as np
from core.node import *
from core.node_socket import *
import os.path
from utils.MECWidgets import SVGLabel

# TODO passar esses metodos para dentro do modulo da porta Serial
class Node_data(Node):

    def __init__(self, scene, title="Bloco dados", parent=None, method=None):
        super().__init__(Node=self)

        self.MODULO = 'Dados'
        self.MODULO_INITIALIZED = False
        self.method = method
        self.scene = scene
        self.parent = parent
        self.title = title

        if method == 'Carregar Arquivo':
            logging.info('Metodo para carregar arquivo de dados')
            self.content = QDMNodeInput(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(300, 300)

            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            inputs = [{'pos': 0.2, 'type': 'str'}]
            outputs = [{'pos': 0.8, 'type': 'float'}]
            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()
        else:

            self.content = QDMNodeData(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(300, 300)

            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

            inputs = [0.15]
            outputs = [0.8]


            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()

    def updateNode(self):
        self.content.refresh()
        self.propagate()




class QDMNodeInput(QWidget):

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QGridLayout()
        self.setLayout(self.layout)



        label_1 = QLabel('IN1 - Diretório')

        entry_1 = QLineEdit()
        entry_1.textEdited.connect(self.node.updateNode)

        self.layout.addWidget(label_1, 0, 0)
        self.layout.addWidget(entry_1, 0, 1)
        checkbox = QCheckBox('Transposto')





        size_data = QLineEdit()
        size_data.setReadOnly(True)

        self.layout.addWidget(checkbox, 1, 0)
        self.layout.addWidget(QLabel('Tamanho'), 2, 0)
        self.layout.addWidget(size_data, 2, 1)




        self.layout.addWidget(QLabel('OUT1 - Dados'), 3, 0)
        checkbox.clicked.connect(self.node.updateNode)

        self.entrys = [entry_1, size_data]
        self.checkbox = [checkbox]



    def refresh(self):
        entrySocket = [{'socket': self.node.inputs[0], 'entry':self.entrys[0]}]

        data = self.node.checkConnectedEdgeData(entrySocket)
        diretorio_arquivo = data[0] if data[0] != '' else None
        if isinstance(diretorio_arquivo, type(None)):
            return 


        if os.path.isfile(diretorio_arquivo):
            self.file_path, self.file_extension = diretorio_arquivo.split('.')

        else:
            return

        if self.file_extension == 'txt':
            try:
                with open(self.file_path+'.'+self.file_extension) as file:
                    data = np.loadtxt(file)
                    if self.checkbox[0].isChecked():
                        self.entrys[1].setText(f'{data.T.shape}')
                        self.node.sendSignal([data.T], [self.node.outputs[0]], [self], ['float'])
                    else:
                        self.entrys[1].setText(f'{data.shape}')
                        self.node.sendSignal([data], [self.node.outputs[0]], [self], ['float'])

            except ValueError as error:
                logging.error(error)
            except IndexError as error:
                logging.error(error)
        if self.file_extension == 'mat':
            try:
                import scipy.io
                data = scipy.io.loadmat(self.file_path+'.'+self.file_extension)
                self.node.sendSignal([data], [self.node.outputs[0]], [self], ['dict'])
                self.node.outputs[0].setColor('dict')
                self.node.propagate()
            except ModuleNotFoundError:
                print('Nao tem a biblioteca para fazer isso')
        else:
            logging.info('Extensão não suportada')
            return





class QDMNodeData(QWidget):

    def __init__(self, node, parent=None):
        self.node = node
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        l1 = QLabel('Porta')
        self.layout.addWidget(l1)

        eof_entry = QLineEdit()
        eol_entry = QLineEdit()
        separator_entry = QLineEdit()
        sol_entry = QLineEdit()
        sof_entry = QLineEdit()

        eof_label = QLabel('EOF')
        eol_label = QLabel('EOL')
        sol_label = QLabel('SOL')
        sof_label = QLabel('SOF')

        separator_label = QLabel('Separador')

        h_frame0 = QFrame()
        h_layout_0 = QHBoxLayout(h_frame0)
        h_layout_0.addWidget(separator_label)
        h_layout_0.addWidget(separator_entry)


        h_frame1 = QFrame()
        h_layout_1 = QHBoxLayout(h_frame1)
        h_layout_1.addWidget(sof_label)
        h_layout_1.addWidget(sof_entry)
        h_layout_1.addWidget(eof_label)
        h_layout_1.addWidget(eof_entry)


        h_frame2 = QFrame()
        h_layout_2 = QHBoxLayout(h_frame2)
        h_layout_2.addWidget(sol_label)
        h_layout_2.addWidget(sol_entry)
        h_layout_2.addWidget(eol_label)
        h_layout_2.addWidget(eol_entry)


        self.layout.addWidget(h_frame0)
        self.layout.addWidget(h_frame1)
        self.layout.addWidget(h_frame2)

        self.entrys = [eof_entry, eol_entry, separator_entry, sol_entry, sof_entry]
    def refresh(self):
        data = self.adjustData()
        print(data)

    def adjustData(self):
        logging.info('Entrei em adjust data')
        data = self.node.inputs[0].edge.data if self.node.inputs[0].hasSignal() else None
        print(data)
        formatted_list = []

        eof = self.entrys[0].text() if  self.entrys[0].text() is not '' else None
        eol = self.entrys[1].text() if self.entrys[1].text() is not '' else None
        separator = self.entrys[2].text() if self.entrys[2].text() is not '' else None
        sol = self.entrys[3].text() if self.entrys[3].text() is not '' else None
        sof = self.entrys[4].text() if self.entrys[4].text() is not '' else None

        try:

            row_separator = eol + sol

            separated_data = data.split(row_separator)
            for index, string_to_format in enumerate(separated_data):

                string_to_format = string_to_format.replace(eol, '')
                string_to_format = string_to_format.replace(sol, '')
                string_to_format = string_to_format.replace(sof, '')
                string_to_format = string_to_format.replace(eof, '')


                formatted_list.append(string_to_format.split(separator))
            formatted_array = np.asarray(formatted_list, dtype=np.float64)
            return formatted_array

        except AttributeError as error:
            print(error)



