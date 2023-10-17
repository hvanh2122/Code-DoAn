import numpy as np

def generate_s_box(key, key_len, round):
    s_box = [0x00] * 256
    irr = [
        0x11B, 0x11D, 0x12B, 0x12D, 0x139, 0x13F, 0x14D, 0x15F, 0x163, 0x165,
        0x169, 0x171, 0x177, 0x17B, 0x187, 0x18B, 0x18D, 0x19F, 0x1A3, 0x1A9,
        0x1B1, 0x1BD, 0x1C3, 0x1CF, 0x1D7, 0x1DD, 0x1E7, 0x1F3, 0x1F5, 0x1F9
    ]
    if round == 0:
        k = 0
        for i in range(key_len):
            k ^= key[i]
        t = k % 0x1e
        irr_pol = irr[t]
        s_box_gen(irr_pol, s_box, k)
    else:
        k = 0
        for i in range(key_len):
            k ^= key[i]
        t = k % 0x1e
        irr_pol = irr[t]
        s_box_gen(irr_pol, s_box, k)

    s_box = array_to_matrix(s_box)

    return s_box

def s_box_gen(irr_pol, s_box, k):
    initialize(irr_pol, s_box, k)  # Initialize and create inversion
    for i in range(16):
        for j in range(16):
            s_box[i * 16 + j] = map(s_box[i * 16 + j])  # Affine transformation

def initialize(irr_pol, s_box, k):
    for i in range(16):
        for j in range(16):
            s_box[i * 16 + j] = inverse((i << 4) + j, irr_pol) ^ k

# Find the inverse multiplication with an irreducible polynomial and build a support table
def inverse(b, irr_pol):
    global r2
    r2 = 0
    if b == 0:
        return 0  # The inverse of 0 is 0
    r0 = irr_pol  # Set r0 to the irreducible polynomial
    r1 = b
    w0 = 0
    w1 = 1
    q = divide(r0, r1)
    w2 = w0 ^ multiply(q, w1, irr_pol)
    while True:
        if r2 == 0:
            break

        r0 = r1
        r1 = r2
        q = divide(r0, r1)
        w0 = w1
        w1 = w2
        w2 = w0 ^ multiply(q, w1, irr_pol)
    return w1

# division
r2 = 0
def divide(a, b):
    global r2
    a_msb = msb(a)
    b_msb = msb(b)

    if a < b:
        r2 = a
        return 0

    bit = a_msb - b_msb
    temp = b << bit
    a ^= temp

    result = (1 << bit) | divide(a, b)
    return result

# Return the highest position with a non-zero value
def msb(num):
    for i in range(9):
        if not (num >> (i + 1)):
            return i
    return 0

# polynomial multiplication in the field GF(2)
def multiply(a, b, irr_pol):
    res = 0
    if b & 0x01:
        res = a
    for i in range(1, 8):
        if b & (0x01 << i):
            temp = a
            for j in range(i):
                if not (temp & 0x80):
                    temp <<= 1
                else:
                    temp <<= 1
                    temp ^= irr_pol
            res ^= temp
    return res

def array_to_matrix(s_box_array):
    # Convert the integer array
    int_array = np.array(s_box_array)

    # Reshape the array to match the s_box shape
    s_box_shape = (16, 16)
    s_box = int_array.reshape(s_box_shape)

    return s_box

# create the inverse S-box
def inv_s_box_gen(s_box):
    s_box = s_box.flatten()
    invs_box = [0x00] * 256
    for i in range(16):
        for j in range(16):
            t = s_box[i * 16 + j]
            x = t >> 4
            y = t & 0x0f
            invs_box[x * 16 + y] = (i << 4) + j
    return array_to_matrix(invs_box)

# Affine transformation
def map(a):
    c = 0x63 # Affine constant
    res = 0x0
    temp = 0x0
    for i in range(8):
        temp ^= ((a >> i) & 0x1) ^ ((a >> ((i + 4) % 8)) & 0x1)
        temp ^= ((a >> ((i + 5) % 8)) & 0x1) ^ ((a >> ((i + 6) % 8)) & 0x1)
        temp ^= ((a >> ((i + 7) % 8)) & 0x1) ^ ((c >> i) & 0x1)
        res |= (temp << i)
        temp = 0x0
    return res
