from core.node import *
from core.node_socket import *
from PyQt5.QtSvg import QSvgWidget
import numpy as np

from scipy import signal, fftpack

from PyQt5.QtWidgets import QCheckBox, QRadioButton


def movavg(x, N=10):
    padded_x = np.insert(np.insert( np.insert(x, len(x), np.empty(int(N/2))*np.nan), 0, np.empty(int(N/2))*np.nan ),0,0)
    n_nan = np.cumsum(np.isnan(padded_x))
    cumsum = np.nancumsum(padded_x)
    window_sum = cumsum[N+1:] - cumsum[:-(N+1)] - x
    window_n_nan = n_nan[N+1:] - n_nan[:-(N+1)] - np.isnan(x)
    window_n_values = (N - window_n_nan)
    movavg = (window_sum) / (window_n_values)
    return movavg

class Node_sigprocess(Node):
    # TODO modificar para ficar somente X(omega) renderizado como output.
    def __init__(self, scene, title="Processamento de Sinais", parent=None, method=None):
        super().__init__(Node=self)
        
        self.method = method # Escolhe qual widget sera mostrado em funcao do botao clicado no módulo
        self.MODULO = method
        self.MODULO_INITIALIZED = False #Parametro utilizado para nomear nas arvores de objetos
        self.parent = parent
        self.scene = scene 
        self.title = method
        self.selected_method = 1
        prosseguir = False

        if method == 'FFT':

            self.content = QDMNodeFFT(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(200, 250)

            inputs = [{'pos': 0.25, 'type': 'float'},
                      {'pos': 0.39, 'type': 'float'}]
            outputs = [{'pos': 0.77, 'type': 'float'},
                       {'pos': 0.87, 'type': 'complex'}]
            prosseguir = True

        if method == 'Média Móvel':

            self.content = QDMNodeSigMediaMovel(self)
            self.grNode = QDMGraphicsNode(self)
            self.grNode.resize(180, 100)

            inputs = [{'pos': 0.63, 'type': 'float'}]
            outputs = [{'pos': 0.63, 'type': 'float'}]
            prosseguir = True

        if prosseguir:
            self.inputs = []
            self.outputs = []
            self.configInputsOutputs(inputs, outputs)
            self.configureObjectTree()
            self.scene.addNode(self)
            self.scene.grScene.addItem(self.grNode)

class QDMNodeSigMediaMovel(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        movavg_le = QLineEdit()
        self.entrys = [movavg_le]
        self.layout.addWidget(QLabel('Ordem'), 0, 0)
        self.layout.addWidget(movavg_le, 0, 1)



    def refresh(self):
        if self.node.inputs[0].hasSignal():
            data = self.node.inputs[0].edge.data
            data_smooth = movavg(data, N=int(self.entrys[0].text()))
            self.node.sendSignal([data_smooth], self.node.outputs, [self], ['float'])

class QDMNodeFFT(QWidget):
    def __init__(self, node, parent=None):
        super().__init__(parent)
        self.node = node
        self.initUI()

    def initUI(self):

        self.layout = QGridLayout()
        self.setLayout(self.layout)

        input_frame = QFrame()
        input_layout = QVBoxLayout(input_frame)

        sockets_texts = ['\Delta t', 'x[k]']
        for cont, socket_text in enumerate(sockets_texts):
             input_layout.addWidget(SVGLabel().load(socket_text, size=(25, 20)))


        self.checkboxes = [QCheckBox('Espectro Duplo'), QCheckBox('Adicionar Zeros')]

        self.layout.addWidget(input_frame)
        for checkbox in self.checkboxes:  self.layout.addWidget(checkbox)

        for label in [SVGLabel().load('f', size=(15, 20)),
                      SVGLabel().load('X(f)', size=(25, 20))]:  self.layout.addWidget(label)


    def refresh(self):

        prosseguir = False
        if (self.node.inputs[0].hasSignal() and
            self.node.inputs[1].hasSignal()):

            prosseguir = True

        if prosseguir:

            dt = self.node.inputs[0].edge.data
            input_signal = self.node.inputs[1].edge.data

            N = len(input_signal)

            L = int(2**np.ceil(np.log2(2*N))) - N if self.checkboxes[1].isChecked() else 0

            f = fftpack.fftfreq(n=N+L, d=dt)
            Xf = dt * fftpack.fft(input_signal, n=N+L)

            if self.checkboxes[0].isChecked(): #Enviar espectro duplo com shift
                self.node.sendSignal([fftpack.fftshift(f), fftpack.fftshift(Xf)],
                                     self.node.outputs,
                                     [self, self],
                                     ['float', 'complex'])
            else:
                self.node.sendSignal([f[:(N+L)//2], Xf[:(N+L)//2]],
                                     self.node.outputs,
                                     [self, self],
                                     ['float', 'complex'])


            # elif self.node.selected_method == 0:
            #     logging.info('Correlação')
            #
            #     R_xx = np.correlate(self.x, self.x, mode='full')
            #     R_xy = np.correlate(self.x, self.y, mode='full')
            #     R_yy = np.correlate(self.y, self.y, mode='full')
            #     tau = range(-len(R_xx)//2, len(R_xx)//2)
            #
            #     self.node.sendSignal([tau, R_xx, R_xy, R_yy],
            #                          self.node.outputs,
            #                          [self, self, self],
            #                          ['float', 'float', 'float'])
            #
            # elif self.node.selected_method == 2:
            #
            #
            #
            #      freqs, S_xx = signal.csd(self.x, self.x, fs=1/dt, nperseg=2**11, nfft=N+L, return_onesided=False)
            #      freqs, S_xy = signal.csd(self.x, self.y, fs=1/dt, nperseg=2**11, nfft=N+L, return_onesided=False)
            #      S_yx = S_xy.conj()
            #      freqs, S_yy = signal.csd(self.y, self.y, fs=1/dt, nperseg=2**11, nfft=N+L, return_onesided=False)
            #
            #      df = freqs[1] - freqs[0]
            #      print(df * sum(S_xx), np.mean(self.x ** 2))
            #      print(df * sum(S_yy), np.mean(self.y ** 2))
            #
            #
            #      self.node.sendSignal([freqs, S_xx.real, S_xy, S_yx, S_yy.real],
            #                           self.node.outputs,
            #                           [self, self, self, self, self],
            #                           ['float', 'float', 'complex', 'complex', 'float'])