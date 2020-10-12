

class Solidmechanics():
    def __init__(self):
        pass

    def stress_tensor(self, stress_dict):

        self.generalized_stress = np.zeros((3, 3))

        for key in stress_dict.keys():
            if key == 'sigma_xx':
                self.generalized_stress[0, 0] = stress_dict[key]
            if key == 'sigma_yy':
                self.generalized_stress[1, 1] = stress_dict[key]
            if key == 'sigma_zz':
                self.generalized_stress[2, 2] = stress_dict[key]

            if key == 'sigma_xy':
                self.generalized_stress[0, 1] = stress_dict[key]
                self.generalized_stress[1, 0] = stress_dict[key]
            if key == 'sigma_xz':
                self.generalized_stress[0, 2] = stress_dict[key]
                self.generalized_stress[2, 0] = stress_dict[key]
            if key == 'sigma_yz':
                self.generalized_stress[1, 2] = stress_dict[key]
                self.generalized_stress[2, 1] = stress_dict[key]

        self.principalstresses()

    def principalstresses(self):
        sigma_p, theta = np.linalg.eig(self.generalized_stress)
        print(sigma_p)


class FiniteElements2D():
    def __init__(self):
        self.vertices = [[0, 0],
                        [0, 1],
                        [1, 0],
                        [1, 1]]


import numpy as np
import sys
sys.path.append('/usr/local/lib/python3.6/dist-packages')
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5 import QtGui
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtWidgets, QtOpenGL



