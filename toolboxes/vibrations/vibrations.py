
import numpy as np
class Sdof():
    def __init__(self):
        pass
    def parameters(self,param_dict):

        if param_dict.__contains__('m'):
            self.m = param_dict['m']
        if param_dict.__contains__('k'):
            self.k = param_dict['k']

        if param_dict.__contains__('omega_n'):
            self.omega_n = param_dict['omega_n']
        else:
            self.omega_n = (self.k/self.m)**0.5
        if param_dict.__contains__('c'):
            self.c = param_dict['c']
            self.zeta = self.c/(2*(self.m*self.omega_n))
        elif param_dict.__contains__('zeta'):
            self.zeta =  param_dict['zeta']
            self.c = self.zeta*2*(self.m*self.k)**0.5

        self.omega_d = self.omega_n*(1 - self.zeta**2)**0.5

    def irf(self):
        print(self.zeta)
        self.h = lambda t: 1/(self.m*self.omega_d)*np.e**(-self.zeta*self.omega_n*t)*np.sin(self.omega_d*t)
    def frf(self):
        self.receptance = lambda Omega: 1/(-self.m*Omega**2 + self.k + 1j*Omega*self.c)
        self.mobility = lambda Omega: 1j*Omega*self.receptance
        self.accelerance = lambda Omega: -Omega**2*self.receptance
