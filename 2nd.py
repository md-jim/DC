import numpy as np
import matplotlib.pyplot as plt

# Input
A = float(input("Amplitude: "))
f = float(input("Frequency: "))
fs = int(input("Sampling rate: "))
T = float(input("Duration: "))

# Analog signal
t = np.linspace(0, T, 1000)
x = A * np.sin(2 * np.pi * f * t)

# Sampling
ts = np.arange(0, T, 1/fs)
xs = A * np.sin(2 * np.pi * f * ts)

# Quantization
L = 8
xq = np.round(xs * L) / L

# Binary encoding
bits = []
for v in xq:
    idx = int((v + A) * (L - 1) / (2 * A))
    bits.append(format(idx, '03b'))

# Output
print("\nBinary Data:")
for b in bits:
    print(b)

# -----------------------------
# Plot
# -----------------------------
plt.figure(figsize=(10,6))

# 1. Analog signal
plt.subplot(3,1,1)
plt.plot(t, x)
plt.title("Analog Signal")
plt.grid()

# 2. Sampling ONLY points (NO analog line)
plt.subplot(3,1,2)
plt.stem(ts, xs, basefmt=" ")
plt.title("Sampling Points Only")
plt.grid()

# 3. Quantized signal
plt.subplot(3,1,3)
plt.step(ts, xq, where='mid')
plt.title("Quantized Signal")
plt.grid()

plt.tight_layout()
plt.show()