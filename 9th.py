# Hamming Code (Error Correction)

# Input
data = input("Enter binary data: ")

# Find number of parity bits
m = len(data)
r = 0

while (2**r < m + r + 1):
    r += 1

# Create empty list
hamming = []

j = 0

# Place data and parity bits (0 placeholders)
for i in range(1, m + r + 1):
    if i & (i - 1) == 0:
        hamming.append(0)
    else:
        hamming.append(int(data[j]))
        j += 1

# Calculate parity bits
for i in range(r):
    pos = 2**i
    count = 0

    for j in range(1, len(hamming)+1):
        if j & pos:
            count += hamming[j-1]

    hamming[pos-1] = count % 2

# Output
print("\nHamming Code:", ''.join(map(str, hamming)))