# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 21:40:34 2019

@author: heito
"""

from LoopClosure import Mechanism
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import cos,sin
from numpy import deg2rad as d2r


mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 16

def Quick(inc,deg,fix):
    o3,X,L1,L2 = inc
    q1       = deg
    R,C,D    = fix
    
    f1 = R*cos(q1) - L1*cos(o3)
    f2 = R*sin(q1) - L1*sin(o3) + C 
    f3 = X - L2*cos(o3)
    f4 = D - L2*sin(o3)
    
    return f1,f2,f3,f4

# Definição do grau de liberdade.
Q1  = d2r(np.r_[0:360:360j])

# Definição de valores conhecidos.
R,C,D = 0.085,0.4,0.75

# Estimativas iniciais.
x0  = d2r(45),0.4,0.4,0.4

# Definição do passo, para uma rotação de 1 passo.
w1  = 1.
h   = np.abs(Q1[0]-Q1[1])/w1

mec = Mechanism(Quick,Q1,[R,C,D],h)

mec.kinematics_solve(x0)

c = ['r','g','c','y']
#o3,X,L1,L2


#Plot de incognitas

fig1, ax = plt.subplots(3,1,figsize=(6,12))

ax[0].plot(Q1,mec.values[0],color='r',label=r'$\theta_3$')
ax[0].set_xlabel('Time (s)')
ax[0].set_ylabel('Rad',color='r')
ax[0].set_title('Position')
ax[0].set_xlim(Q1[0],Q1[-1])
ax[0].tick_params(axis='y',labelcolor='r')

aux = ax[0].twinx()
aux.plot(Q1,mec.values[1],color='b',label=r'$X$')
aux.set_ylabel('m',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[0].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0,fontsize='large')


ax[1].plot(Q1,mec.first[0],color='r',label=r'$\dot\theta_3$')
ax[1].set_xlabel('Time (s)')
ax[1].set_ylabel('Rad/s',color='r')
ax[1].set_title('Velocity')
ax[1].set_xlim(Q1[0],Q1[-1])
ax[1].tick_params(axis='y',labelcolor='r')

aux = ax[1].twinx()
aux.plot(Q1,mec.first[1],color='b',label=r'$\dot X$')
aux.set_ylabel('m/s',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[1].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0,fontsize='large')


ax[2].plot(Q1,mec.secon[0],color='r',label=r'$\ddot \theta_3$')
ax[2].set_xlabel('Time (s)')
ax[2].set_ylabel('Rad/s²',color='r')
ax[2].set_title('Aceleration')
ax[2].set_xlim(Q1[0],Q1[-1])
ax[2].tick_params(axis='y',labelcolor='r')

aux = ax[2].twinx()
aux.plot(Q1,mec.secon[1],color='b',label=r'$\ddot X$')
aux.set_ylabel('m/s²',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[2].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0,fontsize='large')

fig1.tight_layout()
fig1.savefig('inc_quick_return.png',dpi=500)













