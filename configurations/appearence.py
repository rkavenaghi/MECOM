from PyQt5.QtGui import QColor

class Estilos():
    def __init__(self):
        self.pallette = self.default()

    def default(self):
        colors = {'float': QColor("#5fdd31"),
                  'int':   QColor("#b6d7ec"),
                  'str':   QColor("#4f0d20"),
                  'string': QColor("#4f0d20"),
                  'undefined': QColor('#FFFFFF'),
                  'complex': QColor('#f8e17c'),
                  'invalid': QColor('#FF0000'),
                  'boolean': QColor('#0dc2b0'),
                  'input': QColor('#12a99f'),
                  'output': QColor('#3d12ab'),
                  'refresh': QColor('#d0d0d0'),
                  'dict': QColor('#5c8bdb'),
                  'closed': QColor('#0F0F0F')
                  }

        return colors

