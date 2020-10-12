class Rod():
    def __init__(self, *args, **kwargs):

        if 'E' in kwargs.keys():
            self.E = kwargs['E']
        if 'rho' in kwargs.keys():
            self.rho = kwargs['rho']
        if 'L' in kwargs.keys():
            self.L = kwargs['L']
        if 'omega' in kwargs.keys():
            self.omega = kwargs['omega']
        if 'A' in kwargs.keys():
            self.A = kwargs['A']

        self.K_L = self.omega*np.sqrt(self.rho/self.E)
        S_R = self.spectral_element_matrix()


    def spectral_element_matrix(self):
        S_R11 = self.K_L*self.L*1/np.tan(self.K_L*self.L)
        S_R12 = -self.K_L*self.L*1/np.sin(self.K_L * self.L)
        S_R22 = S_R11
        return self.E*self.A/self.L*np.array([[S_R11, S_R12],[S_R12, S_R22]])


if __name__ == '__main__':
    import numpy as np
    import matplotlib.pyplot as plt

    rod1 = Rod(omega=val, E=200e9, rho=1e3, L=1, A=1e-2).spectral_element_matrix()
