from nodes import *
from core.serialization import *
from core import mainmenu
from core.log import *

from core.scene import *
from gui import Toolbar
from gui import style_path, loadStylesheet

from PyQt5.QtWidgets import (QApplication, QPushButton, QWidget, QVBoxLayout, QMainWindow, QFrame,
                             QMdiArea, QDockWidget, QSizePolicy, QPlainTextEdit, QCheckBox, QFileDialog)

from PyQt5.QtCore import Qt
import logging
import sys

import matplotlib.pyplot as plt
plt.rc('mathtext', fontset='cm')

import utils


class ComputationalMecEng(QMainWindow):
    lembretes = []
    database = None
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Engenharia Mecânica Computacional')
        self.list_modules()
        self.current_project = None
        loadStylesheet(style_path())

        self.setGeometry(0, 0, 1800, 1200)
        self.object_names = []
        self.objects = []
        self.statusBar()
        self.mainWidget = QWidget(self)
        self.mainWidget.setFocus()
        self.setCentralWidget(self.mainWidget)
        self.main_layout = QVBoxLayout(self.mainWidget)
        self.mdi = QMdiArea()
        self.toolbar = Toolbar(self)
        self.main_layout.addWidget(self.toolbar.widget)
        self.main_layout.addWidget(self.mdi)        
        self.menu_configuration()
        self.left_panel_treeitens()
        self.show()
        self.database = utils.Database()

    def new_project(self, title='Novo Projeto'):
        self.current_project = NodeEditorWnd(self, title=title)
        self.mdi.addSubWindow(self.current_project)
        self.current_project.resize(self.mdi.width(), self.mdi.height())
        self.current_project.show()
        if isinstance(title, str):
            self.current_project.setWindowTitle(title)

    def saveAsProject(self):
        file_name, _ = QFileDialog.getSaveFileName()
        Serialization(self, currentInstance=self.current_project, sender=self.sender().text(), filename=file_name)
        self.current_project.setWindowTitle(file_name)

    def saveProject(self):
        logging.info('Salvar Projeto')
        Serialization(self, currentInstance=self.current_project, sender=self.sender().text())

    def loadProject(self):
        file_name, _ = QFileDialog.getOpenFileName()
        Serialization(self, sender=self.sender().text(), filename=file_name)
        self.current_project.setWindowTitle(file_name)

    def openRecent(self):
        Serialization(self, sender=self.sender().text())

    def getDockConfigurations(self):
        frame = QFrame()
        layout = QVBoxLayout()
        frame.setLayout(layout)
        frame.adjustSize()
        self.modulesWidget.setWidget(frame)
        return frame, layout

    def list_modules(self):
        self.nodes = {'Processamento de Sinais': self.load_signal_processing,
                      'Vibrações': self.load_vibrations,
                      'Diretório': lambda: Node_string(self.current_project.scene, 'String', parent=self),
                      'Porta Serial': self.load_serial,
                      'Álgebra': self.load_algebra,
                      'Gerador de Sinais': self.load_signals,
                      'Temporizador': lambda: Node_timer(self.current_project.scene, 'Timer', parent=self),
                      'Arquivos CAD': lambda: Node_stl(self.current_project.scene, parent=self),
                      'Complexo': lambda: Node_complex(self.current_project.scene, 'Complexo', parent=self),
                      'Dicionário': lambda: Node_dictionary(self.current_project.scene, parent=self),
                      'Visualização': lambda: Node_graphics(self.current_project.scene, parent=self),
                      'Randômico': lambda: Node_random(self.current_project.scene, 'Random', parent=self),
                      'Data IO': self.load_filedata,
                      #'Mecanismos': self.load_mecanismos,
                      #'Identificação de Sistemas' : self.load_sysid,
                      #'Mecânica dos Sólidos': self.load_solid_mechanics,
                      #'Materiais': lambda: Node_material(self.current_project.scene, parent=self),
                      'Iterador': lambda: Node_iterador(self.current_project.scene, parent=self),
                      'Função': lambda: Node_function(self.current_project.scene, parent=self),
                      'Server': lambda: Node_server(self.current_project.scene, parent=self)}


        self.modules = self.nodes.keys()

    def load_sigprocess(self):
        Node_sigprocess(self.current_project.scene, parent=self, method=self.sender().text())

    def load_solid_mechanics(self):
        frame, layout = self.getDockConfigurations()
        b1 = QPushButton('Desenhar seção')
        b1.clicked.connect(self.load_solid_mechanics_modules)
        layout.addWidget(b1)


    def load_solid_mechanics_modules(self):

        Node_solidmechanics(self.current_project.scene, parent=self, method=self.sender().text())

    def load_sysid(self):
        frame, layout = self.getDockConfigurations()

        b1 = QPushButton('Entrada e Saída')
        b2 = QPushButton('O3KID')

        layout.addWidget(b1)
        layout.addWidget(b2)
        b1.clicked.connect(self.load_sysid_modules)
        b2.clicked.connect(self.load_sysid_modules)


    def load_sysid_modules(self):
        sysidnode.Node_sysid(self.current_project.scene, parent=self, method=self.sender().text())


    def load_mecanismos(self):

        frame, layout = self.getDockConfigurations()

        b1 = QPushButton('Análise Mecanismos')

        b1.clicked.connect(self.load_mecanismos_modules)
        layout.addWidget(b1)


    def load_mecanismos_modules(self):
        Node_mecanismos(self.current_project.scene, parent=self, method=self.sender().text())

    def load_filedata(self):
        frame, layout = self.getDockConfigurations()

        b1 = QPushButton('Data')
        b2 = QPushButton('Carregar Arquivo')

        b1.clicked.connect(self.load_filedata_modules)
        b2.clicked.connect(self.load_filedata_modules)
        layout.addWidget(b1)
        layout.addWidget(b2)

    def load_filedata_modules(self):
        Node_data(self.current_project.scene, parent=self, method=self.sender().text())

    def load_signal_processing(self):

        frame, layout = self.getDockConfigurations()
        

        fft_botao = QPushButton('FFT')
        media_movel = QPushButton('Média Móvel')


        botoes = [fft_botao, media_movel]
        
        for botao in botoes:
            botao.clicked.connect(self.load_sigprocess)
            layout.addWidget(botao)
        self.modulesWidget.show()

    def load_algebra(self):
        self.statusBar().showMessage('Operadores algébricos')
        self.modulesWidget.setWindowTitle('Álgebra')

        frame, layout = self.getDockConfigurations()

        escalar = QPushButton('Escalar')
        adicao = QPushButton('Somatório')
        multiplicacao = QPushButton('Produto')
        convolucao = QPushButton('Convolução')
        inversa = QPushButton('Inversa')
        vetor = QPushButton('Vetor')
        matrix = QPushButton('Matrix')

        botoes = [escalar, adicao, multiplicacao, convolucao, inversa, vetor, matrix]
            
        for cont, botao in enumerate(botoes):
            
            layout.addWidget(botao)
            botao.clicked.connect(self.load_algebra_modules)
        self.modulesWidget.show()

    def load_algebra_modules(self):
        sent_text = self.sender().text()
        if sent_text == 'Vetor':
            Node_array(self.current_project.scene, parent=self)
        elif sent_text == 'Matrix':
            Node_matrix(self.current_project.scene, parent=self)
        elif sent_text == 'Somatório':
            Node_somatorio(self.current_project.scene, parent=self)
        else:
            Node_algebra(self.current_project.scene, parent=self, method=self.sender().text())


    def load_vibrations(self):
        
        self.statusBar().showMessage('Módulo de vibrações')
        self.modulesWidget.setWindowTitle('Módulo de vibrações')
        
        frame, layout = self.getDockConfigurations()
        sdof_button = QPushButton('SDOF')
        botoes = [sdof_button]
            
        for cont, botao in enumerate(botoes):
            botao.clicked.connect(self.load_vibrations_modules)
            layout.addWidget(botao)
        self.modulesWidget.show()

    def load_signals(self):
        self.modulesWidget.setWindowTitle('Módulo de sinais')
        frame, layout = self.getDockConfigurations()

        seno_button = QPushButton('Seno')
        chirp_button = QPushButton('Chirp')
        square_button = QPushButton('PWM')
        impulso_button = QPushButton('Impulso')

        botoes = [seno_button, chirp_button, square_button, impulso_button]

        for botao in botoes:
            layout.addWidget(botao)
            botao.clicked.connect(self.load_signals_module)

        self.modulesWidget.show()

    def load_signals_module(self):
        Node_signals(self.current_project.scene, parent=self, method=self.sender().text())

    def load_vibrations_modules(self):
        Node_vibration(self.current_project.scene, parent=self, method=self.sender().text())



    def load_serial(self):
        self.statusBar().showMessage('Módulo para gerar sinais')
        self.modulesWidget.setWindowTitle('Módulo de Gerenciamento da Porta Serial')
        frame, layout = self.getDockConfigurations()

        serial_button = QPushButton('Configuração da Porta Serial')
        botoes = [serial_button]

        for botao in botoes:
            layout.addWidget(botao)
            botao.clicked.connect(self.load_serial_modules)

        self.modulesWidget.show()

    def load_serial_modules(self):
        Node_serial(self.current_project.scene,parent=self, method=self.sender().text())

    def selected_module(self):
        modulo_str = self.combobox_modules.currentText()
        try:
            self.nodes[self.combobox_modules.currentText()]()

        except Exception as error:
            print(error)
            logging.info('Nao Esta configurado adequadamentee')

    def left_panel_treeitens(self):

        self.modulesWidget = QDockWidget("Módulos", parent = self.mainWidget)
        self.modulesWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.objectsWidget = QDockWidget("Propriedades", parent=self.mainWidget)
        self.objectsWidget.setAllowedAreas(Qt.LeftDockWidgetArea)

        self.loggingWidget = QDockWidget('Log', parent=self.mainWidget)
        self.loggingWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.loggingWidget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.BottomDockWidgetArea)
        self.loggingFrame = QFrame()
        self.loggingLayout = QVBoxLayout()
        self.loggingFrame.setLayout(self.loggingLayout)
        self.loggingWidget.setWidget(self.loggingFrame)

        self.loggingConfigurations()


        left_frame = QFrame()
        layout = QVBoxLayout()

        self.object_tree_documentation_tree_widget = QDMTreeWidgetCustom(parent=self.objectsWidget)
        self.object_tree_documentation_tree_widget.setColumnCount(1)
        self.object_tree_documentation_tree_widget.headerItem().setText(0, 'Objeto')


        
        layout.addWidget(self.object_tree_documentation_tree_widget)
        left_frame.setLayout(layout)

        self.MapDockWidget = QDockWidget('Mapa', parent=self.mainWidget)
        frame = QFrame()
        layout = QGridLayout(frame)
        self.MapDockWidget.minimap = MiniMap()
        layout.addWidget(self.MapDockWidget.minimap)
        self.MapDockWidget.setWidget(frame)



        self.objectsWidget.setWidget(left_frame)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.modulesWidget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.objectsWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.loggingWidget)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.MapDockWidget)


    def loggingConfigurations(self):



        self.loggingWidget.logText = QTextEditLogger(self)
        self.loggingWidget.logText.setFormatter(logging.Formatter(
                                                        '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(self.loggingWidget.logText)
        logging.getLogger().setLevel(logging.INFO)
        self.loggingWidget.widget().layout().addWidget(self.loggingWidget.logText.widget)

        fh = logging.FileHandler('../my-log.log')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s %(module)s %(funcName)s %(message)s'))
        logging.getLogger().addHandler(fh)


    def menu_configuration(self):
        self.mainMenu = mainmenu.initMenu(self)

    def databaseGerenciamento(self):
        item = self.sender()
        if item.text() == 'Visualizar conteúdo':
            if self.database!=None:
                self.database.showContent()



    def lembrete_function(self):

        lembrete = QDialog(self)
        lembrete.setWindowTitle('Lembrete')
        lembrete.setLayout(QVBoxLayout())
        lembrete.plaintextedit = QPlainTextEdit()
        lembrete.layout().addWidget(lembrete.plaintextedit)
        lembrete.setStyleSheet("QWidget {background-color:#CCAAFF}")
        fazendo_cb = QCheckBox('Fazendo')
        finished_cb = QCheckBox('Feito')
        revisado_cb = QCheckBox('Revisado')
        lembrete.checkboxes = [fazendo_cb, finished_cb, revisado_cb]
        for checkbox in [fazendo_cb, finished_cb, revisado_cb]:
            checkbox.stateChanged.connect(self.lembrete_bgcolor)
            lembrete.layout().addWidget(checkbox)
        close_b = QPushButton('Fechar')
        close_b.clicked.connect(lembrete.close)
        lembrete.layout().addWidget(close_b)
        lembrete.checkboxes[0].setChecked(False)
        lembrete.show()
        self.lembretes.append(lembrete)

    def lembrete_bgcolor(self):
        item = self.sender()
        if item.parentWidget().checkboxes[0].isChecked():
            item.parentWidget().setStyleSheet("QWidget {background-color:#CCBBFF}")
        if item.parentWidget().checkboxes[1].isChecked():
            item.parentWidget().setStyleSheet("QWidget {background-color:#CCDDFF}")
        if item.parentWidget().checkboxes[2].isChecked():
            item.parentWidget().setStyleSheet("QWidget {background-color:#CCFFFF}")

    def lembrete_show(self):
        item = self.sender()
        if item.isChecked():
            for lembrete in self.lembretes: 
                lembrete.show()
        else:
            for lembrete in self.lembretes:
                lembrete.hide()

    def minimap_configuration(self):
        if self.sender().isChecked():
            self.Map.show()
        else:
            self.Map.hide()

    def log_menuaction(self):
        if self.sender().isChecked():
            self.loggingWidget.show()
        else:
            self.loggingWidget.hide()

    def module_menuaction(self):
        if self.sender().isChecked():
            self.modules_dock.show()
        else:
            self.modules_dock.hide()

    def properties_menuaction(self):
        if self.sender().isChecked():
            self.objectsWidget.show()
        else:
            self.objectsWidget.hide()

    def helpMenu(self):
        docs = Documentation(parent=self)

    def customizationMenu(self):
        if DEBUG: print('Customizacao do menu')
        """ 
        Ainda não implementado
        
        Permitir que a espessura das linhas sejam modificadas.
        """
        print('Nao implementado')

def run():
    app = QApplication(sys.argv)
    app.setStyle('Breeze')
    window = ComputationalMecEng()
    sys.exit(app.exec_())
if __name__ == "__main__":
    run()



