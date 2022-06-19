state1 = [1,0,1,1]
state2 = [1,0]
state3 = [1,1,1,1,1,1,0]

SBOX1 =[
    [0,1],
    [0,1,2],
    [0,1,2,3],
    [0,1,3,4],
    [1,3,4,5],
    [1,2,4,5],
    [2,4,5,7]]

SBOX2 =[
    [7, 0, 9, 5, 12, 6, 10, 3, 8, 11, 15, 2, 1, 13, 4, 14],
    [8, 3, 5, 9, 11, 12, 6, 10, 1, 13, 2, 14, 4, 7, 15, 0],
    [13, 6, 0, 10, 14, 3, 11, 5, 7, 1, 9, 4, 2, 8, 12, 15],
    [11, 2, 6, 13, 8, 14, 1, 4, 0, 5, 10, 3, 7, 9, 12, 15]]


state_to_dec = int("".join(str(x) for x in state3), 2)
print(state_to_dec,"statetodec")
bits = SBOX1[len(state3) - 2]

for i in range(len(bits)):
    index_col = int("".join(str(state3[x]) for x in bits),2)%16
    index_row = (bits[0] + bits[1] + bits[2] + bits[3])%4

sbox_value = SBOX2[index_row][index_col]


print(bits, index_row, index_col)
print(sbox_value)
print("feedbackbit: ",sbox_value%2)
