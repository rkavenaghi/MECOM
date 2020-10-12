# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:36:43 2019

@author: heito
"""
from numpy import cos, sin

def Four_bar(inc, deg, fix):
    o2,o3 = inc
    q1 = deg
    C1, C2, C3, C4 = fix
    
    f1 = C1*cos(q1) + C2*cos(o2) - C3*cos(o3) - C4
    f2 = C1*sin(q1) + C2*sin(o2) - C3*sin(o3)
    return f1, f2







