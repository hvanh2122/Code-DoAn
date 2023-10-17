import math

def count_ones_zeroes(bits):
    ones = 0
    zeroes = 0
    for bit in bits:
        if int(bit) == 1:
            ones += 1
        else:
            zeroes += 1
    return zeroes, ones


def monobit_test(bits):
    n = len(bits)

    zeroes, ones = count_ones_zeroes(bits)
    s = abs(ones - zeroes)

    p = math.erfc(float(s) / (math.sqrt(float(n)) * math.sqrt(2.0)))

    success = (p >= 0.01)
    return success, p