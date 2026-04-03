from scipy.special import jv
import scipy.constants as sc
import numpy as np
f = 500000000
def energy(R, L, E):
    return (E**2) * sc.epsilon_0 * sc.pi * L * ((R**2)/2) * ((jv(0, 5.52)**2) + (jv(1, 5.52)**2)) 

def pc(R, L, E, Rs):
    eta = np.sqrt((sc.mu_0 / sc.epsilon_0))
    return (((E**2)*sc.pi*Rs)/(eta**2))*((R**2 + R*L)*(jv(1, 5.52)**2)-((R**2)*jv(0, 5.52)*jv(2, 5.52)))  

def Vc(E, L, f):
    w = 2 * sc.pi * f
    return abs(-(sc.c/(1j*w))*(np.exp(1j*w*(L/sc.c))-1))*E*jv(0,0)
V = Vc(2617993.877, 0.3, 499683340)
P = pc(0.5271, 0.3, 2632000, 0.00583188)
U = energy(0.5271, 0.3, 2632000)
Q0 = (2 * np.pi * f * U) / P
rQ = V**2/(2 * np.pi * f * U)
Ra = rQ * Q0
print(f"Vc: {V} V\nPc: {P} W\nEnergy: {U} J\nQuality factor: {Q0}\nR/Q: {rQ} Ohm\nShunt resistance: {Ra} Ohm")
print(900000/0.276)
