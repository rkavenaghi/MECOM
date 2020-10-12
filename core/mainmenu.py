from PyQt5 import QtCore
import PyQt5.Qt as Qt
from PyQt5.QtWidgets import QDockWidget


def groupNodes(application):
    try:
        scene = application.current_project.scene
    except AttributeError:
        print('Não há Cena')
        return

    selected_nodes = []
    for node in scene.nodes:
        if node.grNode.isSelected():
            selected_nodes.append(node)

    openSockets = []
    for node in selected_nodes:
        openSockets.extend(node.getOpenSockets())

    input_sockets = []
    output_sockets = []
    for sockets in openSockets:
        if sockets.position == 'output':
            output_sockets.append(sockets)
        else:
            input_sockets.append(sockets)

    scene.groupNode(selected_nodes, input_sockets, output_sockets)


def sceneMenu(application):
    menu = application.mainMenu.addMenu('Ambiente Gráfico')
    group = menu.addAction('Agrupar nós selecionados')
    group.triggered.connect(lambda: groupNodes(application))


def initMenu(application):
    application.mainMenu = application.menuBar()
    files_menu = application.mainMenu.addMenu('Arquivos')
    new_file = files_menu.addAction('Novo')
    new_file.setShortcut("Ctrl+N")
    new_file.triggered.connect(application.new_project)

    saveFile = files_menu.addAction('Salvar')
    saveFile.setShortcut("Ctrl+S")
    saveAsFile = files_menu.addAction('Salvar como')
    saveAsFile.setShortcut('CTRL+SHIFT+S')
    saveAsFile.triggered.connect(application.saveAsProject)
    saveFile.triggered.connect(application.saveProject)
    loadFile = files_menu.addAction('Abrir')
    loadFile.setShortcut('Ctrl+O')
    loadFile.triggered.connect(application.loadProject)

    openRecent = files_menu.addAction('Abrir Recente')
    openRecent.setShortcut('Ctrl+Shift+R')
    openRecent.triggered.connect(application.openRecent)

    visualizar = application.mainMenu.addMenu('Visualizar')
    panel_show = visualizar.addMenu('Painéis')
    data_show = panel_show.addAction('Dados')
    module_menu = panel_show.addAction('Módulos')
    log_menu = panel_show.addAction('Log')
    properties_menu = panel_show.addAction('Propriedades')
    for item in [data_show, module_menu, log_menu, properties_menu]:
        item.setCheckable(True)
        item.setChecked(True)
    minimap_menu = panel_show.addAction('Mapa')
    minimap_menu.setCheckable(True)
    minimap_menu.setChecked(True)
    minimap_menu.triggered.connect(application.minimap_configuration)

    mostrar_lembrete = visualizar.addAction('Lembretes')
    mostrar_lembrete.setCheckable(True)
    mostrar_lembrete.setChecked(True)
    mostrar_lembrete.triggered.connect(application.lembrete_show)

    log_menu.changed.connect(application.log_menuaction)
    module_menu.changed.connect(application.module_menuaction)
    properties_menu.changed.connect(application.properties_menuaction)
    panel_show.addSeparator()

    fechar = files_menu.addAction('Fechar')
    fechar.setShortcut("Ctrl+Q")
    fechar.triggered.connect(QtCore.QCoreApplication.instance().quit)

    documentation_menu = application.mainMenu.addMenu('Documentação')
    configuration_menu = application.mainMenu.addMenu('Configurações')
    customizacao_menu = configuration_menu.addMenu('Customização')
    customizacao_menu.triggered.connect(application.customizationMenu)
    help_menu = documentation_menu.addAction('Ajuda')
    help_menu.triggered.connect(application.helpMenu)
    lembretes = application.mainMenu.addMenu('Lembretes')
    lembretes.addAction('Adicionar Lembrete').triggered.connect(application.lembrete_function)

    database = application.mainMenu.addMenu('Database')
    database_show = database.addAction('Visualizar conteúdo')
    database_show.triggered.connect(application.databaseGerenciamento)

    colaboration(application)
    sceneMenu(application)

    return application.mainMenu


def colaboration(application):
    """ Socket Programming """

    colab_menu = application.mainMenu.addMenu('Colaborativo')
    chat = colab_menu.addAction('Chat')
    chat.triggered.connect(lambda: chatWidget(application))


def chatWidget(application):
    print(f"Implementar janela de chat no arquivo {__file__} com obj {application}")
    application.chatWidget = QDockWidget("Chat", parent=application.mainWidget)
    application.chatWidget.setSizePolicy(Qt.QSizePolicy.Expanding, Qt.QSizePolicy.Expanding)
    application.chatWidget.setMinimumWidth(300)
    application.addDockWidget(QtCore.Qt.RightDockWidgetArea, application.chatWidget)


