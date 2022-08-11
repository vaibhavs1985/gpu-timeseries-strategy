arr = [135]
for i in range(1,187):
    freq = 0
    if i%2:
        freq = arr[-1]+7
        arr.append(freq)
    else:
        freq = arr[-1]+8
        arr.append(freq)
print(arr)
