import numpy
X = numpy.arange(1, 7, 1)
y = []
rQ = []
i = 1
for j in range(1, 7):
    yy = []
    rr = []
    while i <= 25:
        arquivo = f"({float(i)}, {float(j)}).SFO"
        with open(arquivo, "r") as f:
            lines = f.readlines()
            for line in lines:
                if "Power dissipation" in line:
                    yy.append(float(line.split()[3]))
                if "r/Q" in line: 
                    rr.append(float(line.split()[2]))
        i += 5
    y.append(yy)
    rQ.append(rr)
    i = 1
y = numpy.array(y).T
rQ = numpy.array(rQ).T
#y = y/1000
import matplotlib.pyplot as plt
print(y)
fig, ax = plt.subplots(ncols=2, figsize=(16, 9))
for i, k in enumerate(y):
    ax[0].plot(X, k, label=f"{i + 1} cm")
    
ax[0].set_ylabel("Potencia dissipada")
ax[0].set_xlabel("Raio do beampipe (cm)")
ax[0].set_title("Potencia dissipada")
for i, k in enumerate(rQ):
    ax[1].plot(X, k, label=f"{i + 1} cm")
    
ax[1].set_ylabel("r/Q")
ax[1].set_xlabel("Raio do beampipe (cm)")
ax[1].set_title("r/Q")
plt.legend()
plt.tight_layout()
plt.show() 