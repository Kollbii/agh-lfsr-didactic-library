import textwrap

def split_reduced_key_in_half(key128):
    key_half = len(key128)//2
    left_keys, right_keys = key128[:key_half], key128[key_half:]

    return left_keys, right_keys

def circular_left_shift(bits, numberofbits):
    shiftedbits = bits[numberofbits:] + bits[:numberofbits]
    return shiftedbits

ROUND_SHIFTS = [1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2] #12 round shiftów, ponieważ 12 kluczy

def generate_keys(key128):
    round_keys = list()
    left64, right64 = split_reduced_key_in_half(key128)

    for i in range(len(ROUND_SHIFTS)):

        left64 = circular_left_shift(left64, ROUND_SHIFTS[i])
        right64 = circular_left_shift(right64, ROUND_SHIFTS[i])
        round_keys.append(( left64 + right64))

    return round_keys


EXPANSION_TABLE = [54, 45, 31, 38, 7, 59, 18, 11, 2, 28, 32, 16, 43, 30, 9, 15, 63, 29, 37, 12, 50, 55, 51, 4, 63, 2,
                   27, 59, 32, 39, 0, 13, 37, 53, 2, 62, 26, 14, 44, 60, 62, 60, 43, 11, 3, 21, 63, 50, 11, 5, 20, 58, 26, 56, 53, 40, 19,
                   20, 53, 39, 20, 4, 18, 7, 46, 58, 48, 21, 36, 37, 40, 7, 31, 28, 57, 1, 21, 44, 7, 17, 21, 47, 25, 30, 18, 56, 63, 25,
                   5, 47, 22, 27, 26, 54, 30, 42, 62, 38, 56, 17, 23, 35, 17, 23, 4, 36, 18, 33, 31, 12, 4, 4, 42, 0, 25, 29, 9, 27, 3,
                   17, 12, 61, 36, 44, 13, 51, 54, 9]


def apply_Expansion(expansion_table, bits64):
    """ Rozszerza 64-bitowy blok do 128 bitów, używając zadanego schematu"""
    bits_128 = ""
    for index in expansion_table:
        bits_128 += bits64[index-1]

    return bits_128

def XOR(bits1, bits2):
    # ciągi muszą być równej długości
    xor_result = ""
    for index in range(len(bits1)):
        if bits1[index] == bits2[index]:
            xor_result += '0'
        else:
            xor_result += '1'
    return xor_result

SBOX = [
    # Box-1
    [
        [7, 0, 9, 5, 12, 6, 10, 3, 8, 11, 15, 2, 1, 13, 4, 14],
        [8, 3, 5, 9, 11, 12, 6, 10, 1, 13, 2, 14, 4, 7, 15, 0],
        [13, 6, 0, 10, 14, 3, 11, 5, 7, 1, 9, 4, 2, 8, 12, 15],
        [11, 2, 6, 13, 8, 14, 1, 4, 0, 5, 10, 3, 7, 9, 12, 15]
    ],
    # Box-2
    [
        [8, 2, 13, 3, 4, 15, 11, 7, 0, 10, 1, 14, 5, 6, 12, 9],
        [14, 3, 6, 9, 2, 7, 15, 1, 0, 12, 13, 8, 5, 4, 11, 10],
        [9, 0, 5, 3, 8, 10, 2, 7, 13, 6, 11, 1, 4, 15, 12, 14],
        [12, 15, 5, 2, 3, 10, 0, 13, 7, 4, 14, 11, 6, 9, 1, 8]
    ],
    # Box-3
    [
        [10, 12, 3, 8, 15, 7, 9, 2, 0, 6, 5, 4, 14, 13, 11, 1],
        [6, 8, 9, 11, 15, 14, 12, 0, 10, 4, 7, 13, 3, 1, 5, 2],
        [9, 6, 1, 0, 15, 3, 12, 13, 10, 11, 4, 5, 14, 2, 8, 7],
        [15, 4, 3, 12, 0, 2, 10, 14, 5, 13, 8, 11, 1, 6, 9, 7]
    ],
    # Box-4
    [
        [4, 15, 3, 7, 5, 9, 8, 2, 12, 14, 6, 0, 10, 11, 13, 1],
        [3, 13, 8, 14, 15, 5, 1, 10, 2, 4, 0, 11, 6, 9, 12, 7],
        [9, 13, 10, 6, 3, 11, 15, 0, 7, 2, 14, 12, 8, 4, 5, 1],
        [9, 0, 7, 15, 3, 14, 4, 1, 2, 6, 8, 5, 11, 10, 12, 13]
    ],
    # Box-5
    [
        [6, 11, 14, 5, 13, 9, 3, 15, 10, 12, 4, 2, 1, 7, 8, 0],
        [6, 4, 8, 0, 3, 5, 15, 1, 9, 14, 10, 11, 7, 2, 12, 13],
        [8, 0, 12, 3, 1, 11, 15, 7, 9, 14, 13, 10, 4, 5, 2, 6],
        [5, 10, 15, 13, 6, 7, 11, 2, 0, 9, 4, 8, 14, 3, 12, 1]
    ],
    # Box-6
    [
        [15, 11, 3, 9, 0, 14, 13, 4, 5, 6, 8, 2, 12, 1, 7, 10],
        [11, 4, 8, 1, 7, 15, 14, 10, 2, 13, 5, 6, 12, 3, 9, 0],
        [10, 11, 5, 3, 14, 12, 1, 8, 7, 6, 9, 0, 15, 2, 4, 13],
        [7, 5, 4, 13, 8, 2, 1, 6, 14, 0, 10, 11, 15, 9, 3, 12]
    ],
    # Box-7
    [
        [12, 3, 2, 14, 15, 0, 5, 9, 7, 10, 4, 1, 8, 13, 11, 6],
        [2, 9, 5, 0, 8, 6, 15, 10, 14, 7, 3, 12, 13, 11, 4, 1],
        [6, 8, 15, 2, 12, 5, 3, 14, 10, 1, 9, 4, 7, 11, 0, 13],
        [1, 6, 10, 5, 7, 9, 12, 3, 13, 8, 0, 15, 14, 2, 11, 4]
    ],
    # Box-8
    [
        [15, 4, 12, 2, 14, 1, 8, 5, 9, 3, 11, 7, 6, 0, 10, 13],
        [13, 5, 4, 7, 11, 6, 10, 15, 2, 1, 14, 9, 12, 0, 3, 8],
        [15, 5, 12, 14, 9, 11, 1, 13, 0, 6, 2, 8, 3, 10, 7, 4],
        [3, 2, 6, 13, 0, 7, 9, 1, 5, 12, 4, 8, 14, 11, 15, 10]
    ],
    # Box-9
    [
        [13, 3, 15, 1, 2, 11, 5, 7, 0, 8, 9, 14, 12, 10, 6, 4],
        [5, 6, 9, 10, 11, 13, 7, 12, 14, 2, 1, 0, 4, 8, 3, 15],
        [8, 15, 5, 10, 7, 1, 2, 9, 6, 12, 13, 11, 3, 0, 4, 14],
        [11, 8, 14, 2, 6, 3, 15, 5, 9, 1, 4, 0, 12, 13, 10, 7]
    ],
    # Box-10
    [
        [3, 13, 11, 6, 7, 0, 4, 10, 14, 1, 12, 2, 15, 5, 8, 9],
        [0, 13, 6, 5, 2, 14, 11, 8, 10, 7, 12, 9, 4, 3, 15, 1],
        [9, 10, 13, 15, 11, 12, 5, 7, 0, 14, 4, 3, 2, 1, 6, 8],
        [9, 14, 12, 13, 6, 0, 10, 11, 7, 2, 15, 5, 4, 8, 1, 3]
    ],
    # Box-11
    [
        [7, 10, 5, 1, 14, 4, 8, 3, 12, 15, 6, 9, 11, 13, 2, 0],
        [8, 5, 4, 15, 12, 3, 2, 9, 10, 7, 11, 14, 13, 1, 0, 6],
        [0, 13, 9, 11, 14, 12, 5, 6, 1, 4, 10, 15, 8, 3, 2, 7],
        [11, 1, 3, 14, 5, 10, 2, 0, 15, 12, 9, 7, 6, 13, 4, 8]
    ],
    # Box-12
    [
        [10, 11, 6, 12, 9, 13, 15, 1, 3, 8, 4, 7, 0, 14, 2, 5],
        [2, 7, 14, 4, 1, 8, 13, 5, 9, 11, 6, 3, 15, 12, 0, 10],
        [7, 0, 3, 5, 2, 6, 12, 9, 1, 4, 8, 14, 15, 11, 13, 10],
        [10, 13, 11, 7, 14, 4, 0, 8, 3, 5, 1, 9, 12, 15, 2, 6]
    ]
   
]

def split_128_bits_in_8_bits(block_96_bits):
    block_of_8_bits = textwrap.wrap(block_96_bits, 8)                     #dzielimy 128 bitowy blok na 8 bitowe podbloki.
    return block_of_8_bits

def sbox_get_column_function(block_8_bits):                        
                                                                   
    column_index = XOR(block_8_bits[:4], block_8_bits[4:])          #najpierw xorujemy: bity do czwartego z bitami od czwartego do końca,
    column_index = XOR(column_index, block_8_bits[-6:])             # xorujemy wynik z sześcioma ostatnimi bitami,
    column_index = XOR(block_8_bits[6:], column_index)              # xorujemy ponownie wynik z pierwszyny sześcioma bitami
    column_index = column_index[::-1]                               #na końcu wynik odwracamy

    return column_index

def sbox_get_row_function(block_8_bits):                            #tworzymy ciąg bitów który składa się z: drugiego bitu, XOR 2 bit z 3 bitem,
                                                                    #XOR 4 bit z 5 bitem, oraz z pierwszego bita, cały ciąg pod koniec odwracamy
    row_index = block_8_bits[1] + XOR(block_8_bits[2], block_8_bits[3]) + XOR(block_8_bits[4],block_8_bits[5]) + block_8_bits[0]
    row_index = row_index[::-1]

    return row_index

def binary_to_decimal(binarybits):
    decimal = int(binarybits, 2)                                                #konwersja do wartości dziesiętnej
    return decimal

def decimal_to_binary(decimal):                                                
    binary4bits = bin(decimal)[2:].zfill(4)                                     #usuwanie prefiksu 0b, potem padding do 4 znaków zerami od lewej strony.
    return binary4bits

def sbox_lookup(sboxcount, first_value, second_value):                                
    """ Dostęp do odpowiedniej wartości odpowiedniego sboxa"""

    sbox_row = binary_to_decimal(first_value)                                   #odwołanie do rzędu sbox'a
    sbox_column = binary_to_decimal(second_value)                               #odwołanie do kolumny sboxa
    sbox_value = SBOX[sboxcount][sbox_row][sbox_column]                         #pobranie wartości sboxa[rząd][kolumna] o numerze "sboxcount"

    return decimal_to_binary(sbox_value)

PERMUTATION_TABLE = [40, 10, 34, 2, 42, 8, 63, 24, 50, 14, 37, 32, 58, 27,16, 57, 7, 36, 20, 43, 21, 54,
                    55, 3, 47, 9, 33, 19, 49, 13, 60, 30, 44, 6, 61, 22, 53, 11, 52, 4, 39, 25, 48, 29,
                    38, 12, 62, 28, 45, 17, 51, 1, 41, 15, 35, 23, 59, 26, 64, 5, 46, 18, 56, 31]

def apply_sbox_permutation(permutation_table, sboxes_output):
    permuted64bits = ""
    for index in permutation_table:
        permuted64bits += sboxes_output[index-1]                                    #permutacja sboxów
    return permuted64bits

def functionF(primary_64_bit_block, key_128_bits):
    functionF_64_bit_output = ''
    extended_128_bit_block = apply_Expansion(EXPANSION_TABLE, primary_64_bit_block)      #rozszerzamy początkowy 64 bitowy blok do 128 bitów korzystając z expansion table.

    xor_128_block_key = XOR(extended_128_bit_block, key_128_bits)                       #xor rozszerzonego bloku 96 bitów z kluczem 128 bitów
    sublist_8_bits = split_128_bits_in_8_bits(xor_128_block_key)                        #wejście generowanych podbloków 8 bitowych jest wynikiem XOR-a wyżej.

    result_list_sbox = []
    for i in range(12):                                     #używamy 12 rund, ponieważ 96/8 (taka długość podciągów 8 bitowych stworzonych z 96 bitowego rozszerzonego bloku)
        sbox_column = sbox_get_column_function(sublist_8_bits[i])
        sbox_row = sbox_get_row_function(sublist_8_bits[i])

        result_list_sbox.append(sbox_lookup(i, sbox_column, sbox_row) + sbox_lookup(11 - i, sbox_column, sbox_row))    

    output_joined = "".join(result_list_sbox)                                                       #"składamy" wszystko w jeden string.
    functionF_64_bit_output = apply_sbox_permutation(PERMUTATION_TABLE, output_joined)              #końcowa permutacja sboxów

    return functionF_64_bit_output

INITIAL_PERMUTATION_TABLE = ['122', '114', '106', '98', '90', '82', '74', '66',
                             '124', '116', '108', '100', '92', '84', '76', '68',
                             '126', '118', '110', '102', '94', '86', '78', '70',
                             '128', '120', '112', '104', '96', '88', '80', '72',
                             '121', '113', '105', '97', '89', '81', '73', '65',
                             '123', '115', '107', '99', '91', '83', '75', '67',
                             '125', '117', '109', '101', '93', '85', '77', '69',
                             '127', '119', '111', '103', '95', '87', '79', '71',
                             '58 ', '50 ', '42 ', '34 ', '26 ', '18 ', '10 ', '2',
                             '60 ', '52 ', '44 ', '36 ', '28 ', '20 ', '12 ', '4',
                             '62 ', '54 ', '46 ', '38 ', '30 ', '22 ', '14 ', '6',
                             '64 ', '56 ', '48 ', '40 ', '32 ', '24 ', '16 ', '8',
                             '57 ', '49 ', '41 ', '33 ', '25 ', '17 ', ' 9 ', '1',
                             '59 ', '51 ', '43 ', '35 ', '27 ', '19 ', '11 ', '3',
                             '61 ', '53 ', '45 ', '37 ', '29 ', '21 ', '13 ', '5',
                             '63 ', '55 ', '47 ', '39 ', '31 ', '23 ', '15 ', '7'
                             ]

def apply_permutation(P_TABLE, PLAINTEXT):
    permutated_M = ""
    for index in P_TABLE:
        permutated_M += PLAINTEXT[int(index)-1]
    return permutated_M

def split_bits_in_half(binarybits):
    return binarybits[:len(binarybits)//2], binarybits[len(binarybits)//2:]

INVERSE_PERMUTATION_TABLE = ['104', '72', '112', '80', '120', '88', '128', '96',
                             '103', '71', '111', '79', '119', '87', '127', '95',
                             '102', '70', '110', '78', '118', '86', '126', '94',
                             '101', '69', '109', '77', '117', '85', '125', '93',
                             '100', '68', '108', '76', '116', '84', '124', '92',
                             '99', '67', '107', '75', '115', '83', '123', '91',
                             '98', '66', '106', '74', '114', '82', '122', '90',
                             '97', '65', '105', '73', '113', '81', '121', '89',
                             '40 ', '8 ', '48 ', '16 ', '56 ', '24 ', '64 ', '32',
                             '39 ', '7 ', '47 ', '15 ', '55 ', '23 ', '63 ', '31',
                             '38 ', '6 ', '46 ', '14 ', '54 ', '22 ', '62 ', '30',
                             '37 ', '5 ', '45 ', '13 ', '53 ', '21 ', '61 ', '29',
                             '36 ', '4 ', '44 ', '12 ', '52 ', '20 ', '60 ', '28',
                             '35 ', '3 ', '43 ', '11 ', '51 ', '19 ', '59 ', '27',
                             '34 ', '2 ', '42 ', '10 ', '50 ', '18 ', '58 ', '26',
                             '33 ', '1 ', '41 ', '9 ', '49 ', '17 ', '57 ', '25'
                             ]

# Zamiana na binarne
def get_bin(x, n): return format(x, 'b').zfill(n)

#Zamieniamy listę znaków ASCII na odpowiadającą mu liczbę dziesiętną
def intoIntList(message: str):
    int_array = []
    mesg_array = list(message)

    for i in mesg_array:
        int_array.append(ord(i))

    return int_array

# Zamiana liste liczb int na "stringi binarne"
def intListToBinStr(message_list):
    binary = []

    for x in message_list:
        binary.append(get_bin(x, 8))

    binary_str = ""
    for x in binary:
        binary_str += x

    return binary_str

def encrypt(message, key):
    cipher = ""
    round_keys = generate_keys(key)
    after_ip = apply_permutation(INITIAL_PERMUTATION_TABLE, message)
    L, R = split_bits_in_half(after_ip)

    for i in range(0, 12):                          #sieć feistela, 12 rund.
        L1 = R
        R1 = XOR(L, functionF(R, round_keys[i]))
        L = L1
        R = R1

    RL = R + L
    cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, RL)

    return cipher

def decrypt(message, key):
    cipher = ""
    round_keys = generate_keys(key)
    after_initial_permutation = apply_permutation(INITIAL_PERMUTATION_TABLE, message)
    R, L = split_bits_in_half(after_initial_permutation)

    for i in range(11, -1, -1):

        R1 = L
        L1 = XOR(R, functionF(L, round_keys[i]))
        L = L1
        R = R1

    LR = L + R
    cipher = apply_permutation(INVERSE_PERMUTATION_TABLE, LR)

    return cipher


if __name__ == '__main__':
    # przykład użycia programu:
    message = "szyfrblokowyfeistel"             #minimalna dł. wiadomośći - 16 znaków ASCII
    key = "iQA83SAz$39A&d123123"                #minimalna dł. klucza 16 znaków ASCII

    plaintext = intListToBinStr(intoIntList(message))[:128]
    print("Wiadomość (plaintext, 128 bitów):      ", plaintext)

    binary_key = intListToBinStr(intoIntList(key))[:128]
    print("Klucz (128 bitów):                     ", binary_key)

    ciphertext = encrypt(plaintext, binary_key)
    print("Szyfrogram:                            ", ciphertext)

    decrypted = decrypt(ciphertext, binary_key)
    print("Rozszyfrowana wiadomość:               ", decrypted)

    print("XOR(Plaintext, Rozszyfrowana):         ", XOR(plaintext, decrypted))

