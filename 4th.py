import numpy as np
import matplotlib.pyplot as plt

# Input
Am = float(input("Message Amplitude: "))
fm = float(input("Message Frequency: "))
Ac = float(input("Carrier Amplitude: "))
fc = float(input("Carrier Frequency: "))

# Time
t = np.linspace(0, 1, 1000)

# Message & Carrier
m = Am * np.sin(2*np.pi*fm*t)
c = Ac * np.sin(2*np.pi*fc*t)

# AM
am = (Ac + m) * np.sin(2*np.pi*fc*t)

# FM (simple form)
fm_sig = np.sin(2*np.pi*fc*t + m)

# PM (simple form)
pm = np.sin(2*np.pi*fc*t + np.pi*m)

# Plot
plt.figure(figsize=(10,8))

plt.subplot(5,1,1)
plt.plot(t, m)
plt.title("Message Signal")
plt.grid()

plt.subplot(5,1,2)
plt.plot(t, c)
plt.title("Carrier Signal")
plt.grid()

plt.subplot(5,1,3)
plt.plot(t, am)
plt.title("AM Signal")
plt.grid()

plt.subplot(5,1,4)
plt.plot(t, fm_sig)
plt.title("FM Signal")
plt.grid()

plt.subplot(5,1,5)
plt.plot(t, pm)
plt.title("PM Signal")
plt.grid()

plt.tight_layout()
plt.show()