# -*- coding: utf-8 -*-
"""
Created on Wed Oct  2 18:44:39 2019

@author: heito
"""

from numpy import vander, zeros, r_
from math import factorial
from numpy.linalg import solve
from numpy import sum as nsum



def num_diff(fx,h,t=1,O=8): 
    
    F = Stencil_points(O+1,h,t)
    B = F*(-1)**t
    
    xf = fx[::-1][0:2*O]
    
    
    FN = [f*fx[i:-O+i] for i,f in enumerate(F)]
    BN = [b*xf[i:-O+i] for i,b in enumerate(B)]
    
    FN[-1] = F[-1]*fx[O:]
    BN[-1] = B[-1]*xf[O:]
    
    
    BN = nsum(BN,axis=0)
    FN = nsum(FN,axis=0)
    
    return r_[FN,BN[::-1]]/h**t

def Stencil_points(O,h,t):
    
    n = r_[0:O:1]
    A     = vander(n,increasing=True).T
    b     = zeros((O,1))
    b[t]  = factorial(t)
    C     = solve(A,b)
    
    return C