# -*- coding: utf-8 -*-
"""
Created on Sun Aug 19 17:43:39 2018

@author: heito
"""
from scipy.optimize import fsolve
from numpy import array, exp, ones
from numpy import sum as nsum
from . import stencil

class Mechanism(object):
    
    def __init__(self, loop_eq, deg, fix, time_step, n='single'):
        self.loop_eq = loop_eq
        self.deg = deg
        self.time_step = time_step
        self.fix = fix
        self.values = []
        if n != 'single':
            self.deg = array(deg).T
        
    def kinematics_solve(self, x0):

        for o in self.deg:
            x0 = fsolve(lambda x: self.loop_eq(x, o, self.fix), x0)
            self.values.append(x0)
        
        h = self.time_step
        
        self.values = array(self.values).T
        self.first = array([stencil.num_diff(V, h) for V in self.values])
        self.secon = array([stencil.num_diff(V, h, 2) for V in self.values])
            

def Point(R,ANG,h,frames):
    
    R = [r*ones((frames)) if isinstance(r, float) or isinstance(r,int) else r for r in R]

    position = nsum([r*exp(1j*ang) for r,ang in zip(R,ANG)],axis=0)
    velocity = stencil.num_diff(position, h, 1)
    aceleration = stencil.num_diff(position, h, 2)
    
    return position, velocity, aceleration





    
    
    
    
    
    
    
    
