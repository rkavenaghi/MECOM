# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 16:25:49 2019

@author: heito
"""

from LoopClosure import Mechanism
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from numpy import cos,sin,pi
from numpy import deg2rad as d2r

# %%

mpl.rcParams['xtick.labelsize'] = 14
mpl.rcParams['ytick.labelsize'] = 14
mpl.rcParams['axes.titlesize'] = 16
mpl.rcParams['axes.labelsize'] = 16

def Summing(inc,deg,fix):
    X,L1,L2,o2  = inc
    q1,q2       = deg
    D,C         = fix
    
    f1 = X  - q2 - L1*cos(o2)
    f2 = C  - L1*sin(o2)
    f3 = q1 - X - L2*cos(o2)  
    f4 = D  - L2*sin(o2)
    
    
    return f1,f2,f3,f4

# Definição do grau de liberdade.
ANG  = d2r(np.r_[0:360:360j])
Q1   = 2*(sin(ANG) + 1)
Q2   = 2*(sin(ANG+pi/12) + 1)

# Definição de valores conhecidos. (D,C)
C = 0.15,0.08

# Estimativas iniciais. (B,o2)
x0  = 0.2,0.2,0.2,d2r(150)

# Definição do passo, para uma rotação de 1 passo.
w1  = 1.
h   = np.abs(ANG[0]-ANG[1])/w1

mec = Mechanism(Summing,[Q1,Q2],C,h,2)

mec.kinematics_solve(x0)

c = ['r','g','c','y']
#X,L1,L2,o2

# %%

#Plot de incognitas

fig1, ax = plt.subplots(1,3,figsize=(14,4))

ax[0].plot(ANG,mec.values[3],color='r',label=r'$\theta_2$')
ax[0].set_xlabel('Tempo (s)')
ax[0].set_ylabel('Rad',color='r')
ax[0].set_title('Posição')
ax[0].set_xlim(ANG[0],ANG[-1])
ax[0].tick_params(axis='y',labelcolor='r')

aux = ax[0].twinx()
aux.plot(ANG,mec.values[0],color='b',label=r'$X$')
aux.set_ylabel('m',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[0].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0,fontsize='large')


ax[1].plot(ANG,mec.first[3],color='r',label=r'$\dot\theta_2$')
ax[1].set_xlabel('Tempo (s)')
ax[1].set_ylabel('Rad/s',color='r')
ax[1].set_title('Velocidade')
ax[1].set_xlim(ANG[0],ANG[-1])
ax[1].tick_params(axis='y',labelcolor='r')

aux = ax[1].twinx()
aux.plot(ANG,mec.first[0],color='b',label=r'$\dot X$')
aux.set_ylabel('m/s',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[1].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0,fontsize='large')

ax[2].plot(ANG,mec.secon[3],color='r',label=r'$\ddot \theta_2$')
ax[2].set_xlabel('Tempo (s)')
ax[2].set_ylabel('Rad/s²',color='r')
ax[2].set_title('Aceleração')
ax[2].set_xlim(ANG[0],ANG[-1])
ax[2].tick_params(axis='y',labelcolor='r')

aux = ax[2].twinx()
aux.plot(ANG,mec.secon[0],color='b',label=r'$\ddot X$')
aux.set_ylabel('m/s²',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[2].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0,fontsize='large')

fig1.tight_layout()
fig1.savefig('inc_summing_linkage.png',dpi=500)