# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 12:52:52 2019

@author: heito
"""

from LoopClosure import Mechanism,Point
import numpy as np
import matplotlib.pyplot as plt
from numpy import cos,sin
from numpy import deg2rad as d2r


def Sliding_Four_bar(inc,deg,fix):
    B,o2        = inc
    q1,q2       = deg
    C1,C2,C3    = fix
    
    f1 = C1*cos(q1) + B*cos(o2) - C2*cos(q2) - C3
    f2 = C1*sin(q1) + B*sin(o2) - C2*sin(q2)
    
    
    return f1,f2

# Definição do grau de liberdade.
Q1  = d2r(np.r_[0:360:360j])
Q2  = d2r(np.r_[0:360:360j]*2)

# Definição de valores conhecidos. (C1,C2,C3)
C = 1.5,3,4

# Estimativas iniciais. (B,o2)
x0  = 2.,d2r([30])

# Definição do passo, para uma rotação de 1 passo.
w1  = 1.
h   = np.abs(Q1[0]-Q1[1])/w1

mec = Mechanism(Sliding_Four_bar,[Q1,Q2],C,h,2)

mec.kinematics_solve(x0)

c = ['r','g','c','y']
#B,o2

P = Point([C[0],mec.values[0]],[Q1,mec.values[1]],h,360)

fig1, ax = plt.subplots(1,3,figsize=(14,4))

ax[0].plot(Q1,mec.values[1],color='r',label=r'$\theta_2$')
ax[0].set_xlabel('Tempo (s)')
ax[0].set_ylabel('Rad',color='r')
ax[0].set_title('Posição')
ax[0].set_xlim(Q1[0],Q1[-1])
ax[0].tick_params(axis='y',labelcolor='r')

aux = ax[0].twinx()
aux.plot(Q1,mec.values[0],color='b',label=r'$B$')
aux.set_ylabel('in',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[0].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0)


ax[1].plot(Q1,mec.first[0],color='r',label=r'$\dot\theta_2$')
ax[1].set_xlabel('Tempo (s)')
ax[1].set_ylabel('Rad/s',color='r')
ax[1].set_title('Velocidade')
ax[1].set_xlim(Q1[0],Q1[-1])
ax[1].tick_params(axis='y',labelcolor='r')

aux = ax[1].twinx()
aux.plot(Q1,mec.first[1],color='b',label=r'$\dot B$')
aux.set_ylabel('in/s',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[1].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0)


ax[2].plot(Q1,mec.secon[0],color='r',label=r'$\ddot \theta_2$')
ax[2].set_xlabel('Tempo (s)')
ax[2].set_ylabel('Rad/s²',color='r')
ax[2].set_title('Aceleração')
ax[2].set_xlim(Q1[0],Q1[-1])
ax[2].tick_params(axis='y',labelcolor='r')

aux = ax[2].twinx()
aux.plot(Q1,mec.secon[1],color='b',label=r'$\ddot B$')
aux.set_ylabel('in/s²',color='b')
aux.tick_params(axis='y',labelcolor='b')

lines, labels = ax[2].get_legend_handles_labels()
lines2, labels2 = aux.get_legend_handles_labels()
aux.legend(lines + lines2, labels + labels2, loc=0)

fig1.tight_layout()
fig1.savefig('inc_sliding_four_bar.png',dpi=500)

#Plot pontual

fig2, ax = plt.subplots(1,3,figsize=(14,4))

ax[0].plot(Q1,P[0].real,color='r',label=r'$P_X$')
ax[0].plot(Q1,P[0].imag,color='b',label=r'$P_Y$')
ax[0].set_xlabel('Tempo (s)')
ax[0].set_ylabel(' in')
ax[0].set_title('Posição')
ax[0].legend()
ax[0].set_xlim(Q1[0],Q1[-1])



ax[1].plot(Q1,P[1].real,color='r',label=r'$V_X$')
ax[1].plot(Q1,P[1].imag,color='b',label=r'$V_Y$')
ax[1].set_xlabel('Tempo (s)')
ax[1].set_ylabel('in/s')
ax[1].set_title('Velocidade')
ax[1].legend()
ax[1].set_xlim(Q1[0],Q1[-1])


ax[2].plot(Q1,P[2].real,color='r',label=r'$A_X$')
ax[2].plot(Q1,P[2].imag,color='b',label=r'$A_Y$')
ax[2].set_xlabel('Tempo (s)')
ax[2].set_ylabel('in/s²')
ax[2].set_title('Aceleração')
ax[2].set_xlim(Q1[0],Q1[-1])
ax[2].legend()
ax[2].set_xlim(Q1[0],Q1[-1])

fig2.tight_layout()
fig2.savefig('point_sliding_four_bar.png',dpi=500)







