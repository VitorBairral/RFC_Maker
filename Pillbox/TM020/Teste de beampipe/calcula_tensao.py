import matplotlib.pyplot as plt
import numpy as np
#import pandas as pd
from os import startfile
import time
# Ler r/Q, Q, Pc

def v(rq, q, pc):
    return np.sqrt((q * rq * (pc*1000)))
index = np.arange(1, 25.5, 0.5)
dfs = list() 
for i in range(1, 6):
    U = list()
    w = list()
    Pc = list()
    rQ = list()
    Q = list()
    V = list()
    for j in index:
        arquivo = f"({float(j)}, {float(i)}).SFO"
        with open(arquivo, "r") as f:
            lines = f.readlines()
            next = False
            for line in lines:
                if "Resonant frequency" in line:
                    w.append((float(line.split()[3])))
                if "Stored energy" in line:
                    U.append((float(line.split()[3]))*2)
                if "Power dissipation" in line:
                    Pc.append(float(line.split()[3])*2)
                    next = True
                if "r/Q" in line: 
                    rQ.append(float(line.split()[2])*2)
                if "Q" in line and next:
                    Q.append(float(line.split()[2]))
                    next = False
            V.append(v(Q[-1], rQ[-1], Pc[-1])*2*10e-4)
    
    df = np.array([w, U, Q, Pc, rQ, V])
    dfs.append(df)
radium = range(1, 7)
fig, ax = plt.subplots(ncols=3, nrows=2, figsize=(16, 12))
labels = ["Resonant frequency (mHz)", "Stored Energy (J)", "Q", "Pc (kW)", "r/Q (Ohm)", "V (kV)"]
def print_raio():
    mx = []
    for _ in range(1, 7):
        mx.append(np.zeros(6))
    for i, df in enumerate(dfs):
        for j, var in enumerate(df):
            mx[j][i] = var[-1]
        
    for i, var in enumerate(mx):
        ax[i%2][i//2].plot(radium, var)
        ax[i%2][i//2].set_ylabel(labels[i])
        ax[i%2][i//2].set_xlabel("Comprimento (cm)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig("resultado_raio")
def print_comp():
    for j, df in enumerate(dfs):
        for i, var in enumerate(df):
            ax[i%2][i//2].plot(index, var, label=f"raio = {j + 1} cm")
            ax[i%2][i//2].set_ylabel(labels[i])
            ax[i%2][i//2].set_xlabel("Comprimento (cm)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    plt.savefig("resultado_comp.png")
print_comp()

