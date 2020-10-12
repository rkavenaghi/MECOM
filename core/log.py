from PyQt5.QtWidgets import QPlainTextEdit
import PyQt5.QtCore as QtCore

import logging

class QTextEditLogger(logging.Handler, QtCore.QObject):
    appendPlainText = QtCore.pyqtSignal(str)
    def __init__(self, parent):
        super().__init__()
        QtCore.QObject.__init__(self)
        self.widget = QPlainTextEdit()
        self.widget.setReadOnly(True)
        self.appendPlainText.connect(self.widget.appendPlainText)

    def emit(self, record):
        msg = self.format(record)
        self.appendPlainText.emit(msg)

