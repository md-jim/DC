import numpy as np
import matplotlib.pyplot as plt

# Input
data = input("Enter binary data: ")
bits = [int(b) for b in data]

# NRZ-L
nrz_l = []
for b in bits:
    nrz_l.append(1 if b == 1 else -1)

# NRZ-I
nrz_i = []
level = -1
for b in bits:
    if b == 1:
        level = -level
    nrz_i.append(level)

# RZ
rz = []
for b in bits:
    if b == 1:
        rz += [1, 0]
    else:
        rz += [-1, 0]

# Manchester
manchester = []
for b in bits:
    if b == 1:
        manchester += [1, -1]
    else:
        manchester += [-1, 1]

# AMI
ami = []
level = 1
for b in bits:
    if b == 1:
        ami.append(level)
        level = -level
    else:
        ami.append(0)

# Time
t1 = np.arange(len(bits))
t2 = np.arange(len(rz))
t3 = np.arange(len(manchester))

# Plot
plt.figure(figsize=(10,8))

plt.subplot(5,1,1)
plt.step(t1, nrz_l, where='post')
plt.title("NRZ-L")
plt.grid()

plt.subplot(5,1,2)
plt.step(t1, nrz_i, where='post')
plt.title("NRZ-I")
plt.grid()

plt.subplot(5,1,3)
plt.step(t2, rz, where='post')
plt.title("RZ")
plt.grid()

plt.subplot(5,1,4)
plt.step(t3, manchester, where='post')
plt.title("Manchester")
plt.grid()

plt.subplot(5,1,5)
plt.step(t1, ami, where='post')
plt.title("AMI")
plt.grid()

plt.tight_layout()
plt.show()