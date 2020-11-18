from PyQt5.QtSvg import QSvgWidget
import matplotlib.pyplot as plt
from io import BytesIO
from PyQt5.QtWidgets import QLineEdit
import numpy as np
import logging

def tex2svg(formula, fontsize=12, dpi=300, color='#a0a0a0', figsize=(0.01, 0.01), getsvgfig=False):
    fig = plt.figure(figsize=figsize)
    fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize, color=color)

    if not getsvgfig:
        output = BytesIO()
        fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                    bbox_inches='tight', pad_inches=0.0, frameon=False)
        plt.close(fig)
        output.seek(0)
        return output.read()
    else:
        return fig

class SVGLabel(QSvgWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent

    def tex2svg(self, formula, fontsize=12, dpi=300, color='#a0a0a0'):

        fig = plt.figure(figsize=(0.01, 0.01))
        fig.text(0, 0, r'${}$'.format(formula), fontsize=fontsize, color=color)
        output = BytesIO()
        fig.savefig(output, dpi=dpi, transparent=True, format='svg',
                    bbox_inches='tight', pad_inches=0.0)
        plt.close(fig)
        output.seek(0)
        return output.read()


    def load(self, formula, fontsize=12, dpi=300, figsize=(0.01, 0.01), size=None,  color='#a0a0a0'):
        """


        :param formula:
        :param fontsize:
        :param dpi:
        :param figsize:
        :param size:  Tupla ex.: (30, 30)
        :param color:
        :return:
        """
        super().load(self.tex2svg(formula, fontsize, dpi, color))
        if not isinstance(size, type(None)):
            self.setFixedSize(*size)
        return self


class LineEntryEdit(QLineEdit):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def variables(self):
        ns = {'__builtins__': None, 'pi': np.pi, 'e': np.e}
        for variable in self.parent().node.parent.variables:
            ns.update({variable.content.alias.text(): variable.content.data})
        return ns

    def evaluate(self, value):
        ns = self.variables()
        try:
            signal_data = (eval(value, ns))
            return signal_data
        except TypeError:
            logging.warning('Não é expressão válida')
            return None


if __name__ == '__main__':
    # Usar para auxiliar a escrita de formulas em SVG para a documentacao
    fig = tex2svg('\dot{x} = A x + B u', color='#000000', figsize=(1, 0.15), getsvgfig = True)
    fig.savefig('../resources/filetest.png', dpi=600)