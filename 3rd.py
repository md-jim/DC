import numpy as np
import matplotlib.pyplot as plt

# Input
data = input("Enter binary data: ")
bits = [int(b) for b in data]

samples = 200
A = 1
f0 = 2
f1 = 5

# -----------------------------
# Signals
# -----------------------------
ask, fsk, psk, digital = [], [], [], []

for bit in bits:
    for i in range(samples):
        t = i / samples

        # Digital signal
        digital.append(bit)

        # ASK
        if bit == 1:
            ask.append(np.sin(2*np.pi*f1*t))
        else:
            ask.append(0)

        # FSK
        freq = f1 if bit == 1 else f0
        fsk.append(np.sin(2*np.pi*freq*t))

        # PSK
        phase = 0 if bit == 1 else np.pi
        psk.append(np.sin(2*np.pi*f1*t + phase))

# Time axis
t = np.arange(len(digital))

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10,8))

plt.subplot(4,1,1)
plt.plot(t, digital)
plt.title("Digital Signal")
plt.grid()

plt.subplot(4,1,2)
plt.plot(t, ask)
plt.title("ASK")
plt.grid()

plt.subplot(4,1,3)
plt.plot(t, fsk)
plt.title("FSK")
plt.grid()

plt.subplot(4,1,4)
plt.plot(t, psk)
plt.title("PSK")
plt.grid()

plt.tight_layout()
plt.show()