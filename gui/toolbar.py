from PyQt5.QtWidgets import (QComboBox, QPushButton, QWidget, QVBoxLayout, QFrame, QHBoxLayout)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QSize
import logging


class Toolbar(QWidget):
    TOOLBAR_HEIGHT = 100
    BUTTON_SIZE = QSize(40, 40)
    ICON_SIZE = QSize(40, 40)

    def __init__(self, reference):
        super().__init__()
        self.App = reference
        self.widget = self.ui()

    def ui(self):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        undo_button = QPushButton()
        redo_button = QPushButton()
        text_button = QPushButton('T')

        for buttons in [undo_button, redo_button, text_button]:
            buttons.setFixedSize(self.BUTTON_SIZE)
            buttons.setIconSize(self.ICON_SIZE)

        undo_button.setIcon(QIcon("resources/icons/undo.svg"))

        redo_button.setIconSize(self.ICON_SIZE)
        redo_button.setIcon(QIcon("resources/icons/redo.svg"))

        undo_button.clicked.connect(self.undo_event)
        redo_button.clicked.connect(self.redo_event)
        text_button.clicked.connect(self.textInScene)

        layout.addWidget(undo_button)
        layout.addWidget(redo_button)
        layout.addWidget(text_button)
        frame.setFixedHeight(self.TOOLBAR_HEIGHT)

        modules_frame = QFrame()
        frame_layout = QVBoxLayout(modules_frame)

        self.App.combobox_modules = QComboBox()

        self.App.combobox_modules.addItem('selecione um módulo')
        self.App.combobox_modules.addItems(self.App.modules)
        self.App.combobox_modules.model().item(0).setEnabled(False)
        self.App.combobox_modules.currentIndexChanged.connect(self.App.selected_module)

        frame_layout.addWidget(self.App.combobox_modules)

        layout.addWidget(modules_frame)
        return frame


    def textInScene(self):
        logging.info('Escrever um texto na SCENE')

    def hasScene(self):
        if hasattr(self.App.current_project, 'scene'):
            return 1
        else:
            return 0

    def undo_event(self):
        if self.hasScene():
            self.App.current_project.scene.history.undo()

    def redo_event(self):
        if self.hasScene():
            self.App.current_project.scene.history.redo()
