welcome_str = f""" 
MecEngComputacional
Versão = 0.001  
Autor: Renan Cavenaghi Silva
Contato: rkavenaghi@gmail.com

Diretório: {__file__}
Repositório: https://github.com/rkavenaghi/MecEngCom
"""

SHOW_MESSAGE = 1
if SHOW_MESSAGE:
    print(welcome_str)


import sys
import os
sys.path.append(os.path.dirname(__file__))
from gui import application


application.run()
