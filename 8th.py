# Checksum Error Detection

def binary_addition(a, b):
    result = bin(int(a, 2) + int(b, 2))[2:]

    # Carry handling
    while len(result) > 4:
        carry = result[:-4]
        result = bin(int(result[-4:], 2) + int(carry, 2))[2:]

    return result.zfill(4)


# User Input
n = int(input("Enter number of data blocks: "))

data = []

for i in range(n):
    block = input(f"Enter 4-bit block {i+1}: ")
    data.append(block)

# Add all blocks
checksum = "0000"

for block in data:
    checksum = binary_addition(checksum, block)

# 1's Complement
checksum = ''.join('1' if bit == '0' else '0' for bit in checksum)

print("Checksum:", checksum)