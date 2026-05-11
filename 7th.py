# CRC Program in Python

def xor(a, b):
    result = ""

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"

    return result


def mod2div(dividend, divisor):

    pick = len(divisor)

    temp = dividend[0:pick]

    while pick < len(dividend):

        if temp[0] == '1':
            temp = xor(divisor, temp) + dividend[pick]

        else:
            temp = xor('0' * pick, temp) + dividend[pick]

        pick += 1

    if temp[0] == '1':
        temp = xor(divisor, temp)
    else:
        temp = xor('0' * pick, temp)

    return temp


# -----------------------------
# User Input
# -----------------------------
data = input("Enter data bits: ")
divisor = input("Enter divisor: ")

# Append zeros
zeros = '0' * (len(divisor) - 1)
dividend = data + zeros

# Calculate CRC remainder
remainder = mod2div(dividend, divisor)

# Final transmitted code
codeword = data + remainder

# -----------------------------
# Output
# -----------------------------
print("CRC Remainder :", remainder)
print("Transmitted Codeword :", codeword)