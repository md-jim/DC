# Longitudinal Redundancy Check (LRC)

# Input
n = int(input("Enter number of binary words: "))

data = []
for i in range(n):
    word = input(f"Enter binary word {i+1}: ")
    data.append(word)

# Find length of words
length = len(data[0])

# LRC calculation
lrc = ""

for i in range(length):
    count = 0

    for j in range(n):
        if data[j][i] == '1':
            count += 1

    # Even parity
    if count % 2 == 0:
        lrc += '0'
    else:
        lrc += '1'

# Output
print("\nData Words:")
for w in data:
    print(w)

print("\nLRC Code:", lrc)