import math
import scipy.special as ss
from fractions import Fraction


def frequency_within_block_test(input):
    M = 4
    n =len(input)
    # fieldnames = ['number','chisq','p-value', 'success']

    N = int(math.floor(n / M))

    if N > 15:
        N = 15
        M = int(math.floor(n / N))

    if n < 5:
        # Too little data for test. Input of length at least 100 bits required
        return False,  0.0

    num_of_blocks = N

    block_size = M

    proportions = list()

    for i in range(num_of_blocks):
        block = input[i * (block_size):((i + 1) * (block_size))]

        ones = block.count('1')

        zeroes = block.count('0')

        proportions.append(Fraction(ones, block_size))

    chisq = 0.0

    for prop in proportions:
        chisq += 4.0 * block_size * ((prop - Fraction(1, 2)) ** 2)

    p = ss.gammaincc((num_of_blocks / 2.0), float(chisq) / 2.0)  # p-value

    success = (p >= 0.01)

    return success, p


if __name__ == '__main__':
    bits = '11110010010001101000110111111000011001110111110111100000110010111101011111010011000001110001010100101111101001100000111000101'
    frequency_within_block_test(bits)