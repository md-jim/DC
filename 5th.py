# Lab-5
# Vertical Redundancy Check (VRC)
# Python Program

# -----------------------------
# User Input
# -----------------------------
data = input("Enter binary data: ")

# -----------------------------
# Count number of 1's
# -----------------------------
count = data.count('1')

# -----------------------------
# Generate Parity Bit
# -----------------------------
if count % 2 == 0:
    parity = '0'      # Even parity
else:
    parity = '1'

# -----------------------------
# Append Parity Bit
# -----------------------------
vrc_code = data + parity

# -----------------------------
# Output
# -----------------------------
print("\nOriginal Data :", data)
print("Parity Bit    :", parity)
print("VRC Code      :", vrc_code)