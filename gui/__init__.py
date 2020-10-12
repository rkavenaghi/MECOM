from .toolbar import Toolbar
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QFile
import configurations

print(f'Carregando configurações de estilo de {__file__}')


def style_path():
    return configurations.__path__[0]+'/qss/nodestyle.qss'


def loadStylesheet(filename):
    file = QFile(filename)
    file.open(QFile.ReadOnly | QFile.Text)
    stylesheet = file.readAll()
    QApplication.instance().setStyleSheet(str(stylesheet, encoding='utf-8'))
